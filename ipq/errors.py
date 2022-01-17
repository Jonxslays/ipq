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
"""ipq error module."""

from __future__ import annotations

from typing import Any


class IpqError(Exception):
    """Base exception all ipq errors inherit from."""

    def __init__(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.message = message
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return f"\033[1;31mError\033[0m: {self.message}"


class ShellCommandError(IpqError):
    """Raised when something goes wrong with a shell command."""


class InvalidWhoisData(ShellCommandError):
    """Raised when invalid data is returned from the `whois` command."""


class MissingWhois(ShellCommandError):
    """Raised when the `whois` command is not present."""


class MissingNSLookup(ShellCommandError):
    """Raised when the `nslookup` command is not present."""


class InvalidHost(ShellCommandError):
    r"""Raised when host does not match domain or IP regex.

    -Domain-: `^((?!-)[\w\d-]{1,63}(?<!-)\.)+[a-zA-Z][\w]{1,5}$`
    ---IP---: `^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$`
    """
