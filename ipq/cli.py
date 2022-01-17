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

from __future__ import annotations

import typing as t
from queue import Queue
from threading import Thread

import click

from ipq import __packagename__, __version__, errors, models, utils


@click.command(__packagename__)
@click.version_option(__version__, "-v", "--version", prog_name=__packagename__)
@click.help_option("-h", "--help")
@click.argument("host", type=str, nargs=1)
@click.option("-w", "--whois", is_flag=True, help="Include WHOIS data in results.")
@click.option("-p", "--ping", is_flag=True, help="Ping the host.")
def invoke(host: str, whois: bool, ping: bool) -> None:
    """Quickly gather IP and domain name information."""
    targets: list[t.Type[models.IPData] | t.Type[models.WhoisData]] = [models.IPData]
    queue: Queue[str] = Queue(2)
    threads: list[Thread] = []
    output: list[str] = []
    domain = utils.DOMAIN_RGX.match(host)
    ip = utils.IP_RGX.match(host)

    if not domain and not ip:
        raise errors.InvalidHost(f"{host!r} is not a valid domain or IP address.")

    if ping:
        raw_ping = models.PingData.new(host, 1)
        print(raw_ping.data)
        return None

    if ip and whois:
        raise errors.InvalidHost(f"You must pass a domain as the host for the '-w' flag.")

    if whois:
        targets.append(models.WhoisData)

    for obj in targets:
        thread = Thread(target=obj.new, args=(queue, host))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    while not queue.empty():
        output.append(queue.get())

    print("\n".join(output))
