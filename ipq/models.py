# Copyright (c) 2022-present Jonxslays

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""Models the various data retrieved by ipq."""

from __future__ import annotations

import re
import shutil
import subprocess
import typing as t
from dataclasses import dataclass, field

from ipq import errors

T = t.TypeVar("T", str, list[str])


@dataclass(slots=True)
class WhoisData:
    """Represents a domains whois info."""

    domain: str = ""
    registrar: str = ""
    created: str = ""
    updated: str = ""
    expires: str = ""
    status: str = ""
    nameservers: list[str] = field(default_factory=list)

    @classmethod
    def new(cls, domain: str) -> WhoisData:
        """Creates a new `WhoisData` object with the whois command."""
        if not shutil.which("whois"):
            raise errors.MissingWhois("ipq requires the `which` command, please install it.")

        self = cls()
        proc = subprocess.run(["whois", domain.lower()], capture_output=True)
        data = proc.stdout.decode("utf-8")
        return self._black_magic(data.lower())

    @staticmethod
    def _str_rgx(q: str, data: str) -> str | None:
        """Parses for values that can only occur once."""
        rgx = re.compile(f"^\\s*{q}: (.*)$", re.M)

        if buf := rgx.search(data):
            return buf.group(1)

        return None

    @staticmethod
    def _ns_rgx(q: str, data: str) -> list[str] | None:
        """Parses for nameservers, which the can be multiple of."""
        rgx = re.compile(f"^\\s*{q}: (.*)$", re.M)

        if ns := rgx.findall(data):
            return [*set(ns)] # prevents duplicate nameservers in the list

        return None

    @staticmethod
    def _maybe(value: T | None) -> T:
        """Returns the value, or the appropriate replacement if None."""
        if isinstance(value, list):
            return value or []

        elif isinstance(value, str):
            return value or "Not Found"

        # We should *hopefully* never get here
        raise errors.InvalidWhoisData("Whois did not return valid data.")

    def __str__(self) -> str:
        return (
            "========== WHOIS ==========\n"
            f"Domain: {self.domain}\n"
            f"Registrar: {self.registrar}\n"
            f"Created: {self.created}\n"
            f"Updated: {self.updated}\n"
            f"Expires: {self.expires}\n"
            f"Status: {self.status}\n"
            f"Nameservers: {', '.join(self.nameservers)}\n"
            "==========================="
        )

    def _black_magic(self, data: str) -> WhoisData:
        """Sets all the data to the appropriate attr on this obj."""
        attr_map: dict[str, str] = {
            "domain": "domain name",
            "registrar": "registrar",
            "created": "creation date",
            "updated": "updated date",
            "status": "domain status",
            "expires": "registry expiry date",
            "nameservers": "name server",
        }

        for k, v in attr_map.items():
            if v == "name server":
                setattr(self, k, self._maybe(self._ns_rgx(v, data)))

            else:
                setattr(self, k, self._maybe(self._str_rgx(v, data)))

        return self


@dataclass(slots=True)
class IPData:
    """Represents information about the given IP."""

    ip: str
    hostname: str
    city: str
    region: str
    country: str
    loc: str
    org: str
    postal: str
    timezone: str
