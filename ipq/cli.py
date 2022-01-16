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
"""Command line argument parser."""

import re

import click

from ipq import errors, models, __packagename__, __version__

DOMAIN_RGX = re.compile(r"^((?!-)[\w\d-]{1,63}(?<!-)\.)+[a-zA-Z][\w]{1,5}$")
IP_RGX = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")


@click.command(__packagename__)
@click.version_option(__version__, "-v", "--version", prog_name=__packagename__)
@click.help_option("-h", "--help")
@click.argument("host", type=str, nargs=1)
@click.option("-w", "--whois", is_flag=True, help="Include WHOIS data in results.")
def invoke(host: str, whois: bool) -> None:
    """Workhorse function that creates objects and parses CLI args."""
    dom_match = DOMAIN_RGX.match(host)
    ip_match = IP_RGX.match(host)

    if not dom_match and not ip_match:
        raise errors.InvalidHost(f"{host!r} is not a valid domain or IP address.")

    if whois:
        _w = models.WhoisData.new(host)
        print(_w)
