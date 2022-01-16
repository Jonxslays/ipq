# Copyright (c) 2022-present Jonxslays

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Models the various data retrieved by ipq."""

from __future__ import annotations

import re
import subprocess
import typing as t
from dataclasses import dataclass, field


T = t.TypeVar("T", str, list[str])


@dataclass
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
        self = cls()
        proc = subprocess.run(["whois", domain.lower()], capture_output=True)
        data = proc.stdout.decode("utf-8")
        return self._black_magic(data.lower())

    @staticmethod
    def _str_rgx(q: str, data: str) -> str | None:
        rgx = re.compile(f"^\\s*{q}: (.*)$", re.M)

        if buf := rgx.search(data):
            return buf.group(1)

        return None

    @staticmethod
    def _ns_rgx(q: str, data: str) -> list[str] | None:
        rgx = re.compile(f"^\\s*{q}: (.*)$", re.M)

        if ns := rgx.findall(data):
            return ns

        return None

    @staticmethod
    def _maybe(value: T | None) -> T:
        if isinstance(value, list):
            return value or []

        elif isinstance(value, str):
            return value or "Not Found"

        # We should *hopefully* never get here
        raise RuntimeError("Whois did not return valid data.")

    def _black_magic(self, data: str) -> WhoisData:
        attr_map: dict[str, t.Any] = {
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


@dataclass
class IPData:
    ...
