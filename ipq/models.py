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

import os
import re
import subprocess
import typing as t
from dataclasses import dataclass, field
from queue import Queue

from ipq import errors, utils

T = t.TypeVar("T", str, list[str])
CYAN = utils.Colors.CYAN
STOP = utils.Colors.STOP
GREEN = utils.Colors.GREEN
PURPLE = utils.Colors.PURPLE
YELLOW = utils.Colors.YELLOW


@dataclass(slots=True)
class WhoisData:
    """Represents a domains whois info."""

    queue: Queue[str]
    domain: str = ""
    registrar: str = ""
    created: str = ""
    updated: str = ""
    expires: str = ""
    status: list[str] = field(default_factory=list)
    nameservers: list[str] = field(default_factory=list)

    @classmethod
    def new(cls, queue: Queue[str], host: str) -> WhoisData:
        """Creates a new `WhoisData` object with the whois command."""
        self = cls(queue)
        self._black_magic(self._whois(host).lower())
        self.queue.put(str(self))
        return self

    @staticmethod
    def _rgx(q: str, data: str) -> str | None:
        """Parses for values that can only occur once."""
        rgx = re.compile(f"^\\s*{q}: (.*)$", re.M)
        match = rgx.search(data)
        return match.group(1) if match else None

    @staticmethod
    def _greedy_rgx(q: str, data: str) -> list[str] | None:
        """Parses for nameservers, which the can be multiple of."""
        rgx = re.compile(f"^\\s*{q}: (.*)$", re.M)
        match = rgx.findall(data)
        return [*set(match)] if match else None

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
        status = "\n".join(f" - {s.split()[0]}" for s in self.status)
        ns = "\n".join(f" - {n}" for n in self.nameservers)

        return (
            f"{YELLOW}==========={STOP} {GREEN}WHOIS{STOP} {YELLOW}===========\n{STOP}"
            f"{CYAN}Domain:       {self.domain}\n{STOP}"
            f"{PURPLE}Registrar:    {self.registrar}\n{STOP}"
            f"{CYAN}Created:      {self.created}\n{STOP}"
            f"{PURPLE}Updated:      {self.updated}\n{STOP}"
            f"{CYAN}Expires:      {self.expires}\n{STOP}"
            f"{PURPLE}Nameservers:  \n{ns}\n{STOP}"
            f"{CYAN}Status:\n{status}\n{STOP}"
            f"{YELLOW}============================={STOP}"
        )

    @utils.requires("whois")
    def _whois(self, host: str) -> str:
        """Makes a call to the whois command."""
        proc = subprocess.run(["whois", host.lower()], capture_output=True)
        return proc.stdout.decode("utf-8")

    def _black_magic(self, data: str) -> None:
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
            if k in ("nameservers", "status"):
                setattr(self, k, self._maybe(self._greedy_rgx(v, data)))

            else:
                setattr(self, k, self._maybe(self._rgx(v, data)))


@dataclass(slots=True)
class IPData:
    """Represents information about the given IP."""

    queue: Queue[str]
    ip: str = ""
    hostname: str = ""
    city: str = ""
    country: str = ""
    org: str = ""
    postal: str = ""

    @classmethod
    def new(cls, queue: Queue[str], host: str) -> IPData:
        """Creates a new IP Data object for the given host."""
        self = cls(queue)

        if utils.DOMAIN_RGX.match(host):
            self.ip = self._ns_lookup(host, utils.NSLOOKUP_IP_RGX)

        elif utils.IP_RGX.match(host):
            self.ip = host

        else:
            raise errors.ShellCommandError(f"{host!r} is not a valid domain or IP address.")

        try:
            self.hostname = self._ns_lookup(self.ip, utils.NSLOOKUP_HOST_RGX)
        except errors.ShellCommandError:
            self.hostname = "Not Found"

        self._red_magic(self.ip)
        self.queue.put(str(self))
        return self

    def __str__(self) -> str:
        return (
            f"{YELLOW}=========={STOP} {GREEN}IP INFO{STOP} {YELLOW}==========\n{STOP}"
            f"{CYAN}IP:           {self.ip}\n{STOP}"
            f"{PURPLE}Hostname:     {self.hostname}\n{STOP}"
            f"{CYAN}City:         {self.city}\n{STOP}"
            f"{PURPLE}Country:      {self.country}\n{STOP}"
            f"{CYAN}Postal code:  {self.postal}\n{STOP}"
            f"{PURPLE}Organization: {self.org}\n{STOP}"
            f"{YELLOW}============================={STOP}"
        )

    @utils.requires("whois")
    def _red_magic(self, host: str) -> str:
        """Sets all the data to the appropriate attr on this obj."""
        attr_map: dict[str, str] = {
            "city": "City",
            "country": "Country",
            "org": "OrgName",
            "postal": ".*Postal\\s?Code",
        }

        proc = subprocess.run(["whois", host], capture_output=True)
        data = proc.stdout.decode("utf-8")

        for k, v in attr_map.items():
            rgx = re.compile(f"^{v}:\\s+(.*)$", re.M)
            match = rgx.search(data)
            setattr(self, k, match.group(1) if match else "Not Found")

        return ""

    @utils.requires("nslookup")
    def _ns_lookup(self, host: str, rgx: re.Pattern[str]) -> str:
        """Runs the nslookup command and returns a regex match."""
        proc = subprocess.run(["nslookup", host.lower()], capture_output=True)
        data = proc.stdout.decode("utf-8")
        match = rgx.search(data)

        if not match:
            raise errors.ShellCommandError(f"Something went wrong with 'nslookup' for {host!r}")

        return match.group(1)


@dataclass(slots=True)
class PingData:
    """Data received from pinging the host."""

    data: str = ""

    @classmethod
    def new(cls, host: str, count: int) -> PingData:
        self = cls()

        proc = subprocess.run(
            ["ping", "-n" if os.name == "nt" else "-c", f"{count}", host.lower()],
            capture_output=True,
        )

        self.data = proc.stdout.decode("utf-8")
        return self
