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
"""Command line argument parser."""

import asyncio
import re

import click


DOMAIN_RGX = re.compile(r"^((?!-)[\w\d-]{1,63}(?<!-)\.)+[a-zA-Z][\w]{1,5}$")
IP_RGX = re.compile(r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(:\d{1,5})?$")


class Runner:
    __slots__ = "host"

    def __init__(self, host: str) -> None:
        self.host = host

    async def execute(self) -> None:
        if ip := re.match(IP_RGX, self.host):
            print("its an ip", ip.string)
            return None

        if domain := re.match(DOMAIN_RGX, self.host):
            print("its a domain", domain.string)
            return None

        print("not a real domain or ip")


@click.command(name="ipq")
@click.version_option()
@click.argument("host", type=str, nargs=1)
def invoke(host: str) -> None:
    asyncio.run(Runner(host).execute())
