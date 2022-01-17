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
"""ipq utility functions."""

from __future__ import annotations

import functools
import re
import shutil
import typing as t

from ipq import errors

ReturnT = t.Callable[..., str]
RequiresT = t.Callable[[ReturnT], ReturnT]


DOMAIN_RGX = re.compile(r"^((?!-)[\w\d-]{1,63}(?<!-)\.)+[a-zA-Z][\w]{1,5}$")
IP_RGX = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
NSLOOKUP_IP_RGX = re.compile(r"\n\nNon-authoritative answer:\n.*\nAddress: (.*)\n")
NSLOOKUP_HOST_RGX = re.compile(r"name = (.*)\n")


@functools.lru_cache
def check_availability(command: str) -> bool:
    """Checks whether the given command is on the system."""
    return shutil.which(command) is not None


def requires(*commands: str) -> RequiresT:
    """Decorator to require the given commands."""

    def inner(func: ReturnT) -> ReturnT:
        """Decorates the function and checks for the commands."""
        for command in commands:
            if not check_availability(command):
                raise errors.MissingWhois(
                    f"ipq requires the {command!r} command, please install it."
                )

        @functools.wraps(func)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> str:
            """Wraps and executes the decorated function."""
            return func(*args, **kwargs)

        return wrapper

    return inner


class Colors:
    __slots__ = ()

    STOP = "\033[0m"
    RED = "\033[1;31m"
    GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[1;34m"
    PURPLE = "\033[1;35m"
    CYAN = "\033[1;36m"
