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
"""A CLI tool for gathering IP and domain name information."""

from __future__ import annotations

__all__ = ["cli", "errors", "models", "utils"]

__packagename__ = "ipq"
__version__ = "0.1.1"
__author__ = "Jonxslays"
__copyright__ = "2022-present Jonxslays"
__description__ = "A CLI tool for gathering IP and domain name information."
__url__ = "https://github.com/Jonxslays/ipq"
__repository__ = __url__
__license__ = "MIT"

from . import cli, errors, models, utils
