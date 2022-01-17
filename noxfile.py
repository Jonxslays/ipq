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

from __future__ import annotations

from pathlib import Path

import nox
import toml


def get_dependencies() -> dict[str, str]:
    with open("pyproject.toml") as f:
        data = toml.loads(f.read())["tool"]["poetry"]
        deps = data["dev-dependencies"]
        deps.update(data["dependencies"])

    return dict((k.lower(), f"{k}{v}".replace("^", "~=")) for k, v in deps.items())


DEPS = get_dependencies()


@nox.session(reuse_venv=True)
def types(session: nox.Session) -> None:
    session.install("-U", DEPS["pyright"], DEPS["mypy"], DEPS["click"])
    session.run("mypy", "ipq")
    session.run("pyright")


@nox.session(reuse_venv=True)
def formatting(session: nox.Session) -> None:
    session.install("-U", DEPS["black"], DEPS["len8"])
    session.run("black", ".", "--check")
    session.run("len8")


@nox.session(reuse_venv=True)
def imports(session: nox.Session) -> None:
    session.install("-U", DEPS["flake8"], DEPS["isort"])
    session.run("isort", "ipq", "tests", "-cq")
    session.run(
        "flake8",
        "ipq",
        "tests",
        "--select",
        "F4",
        "--extend-ignore",
        "E,F",
        "--extend-exclude",
        "__init__.py,",
    )


@nox.session(reuse_venv=True)
def licensing(session: nox.Session) -> None:
    missing: list[Path] = []
    files: list[Path] = [
        *Path("./ipq").rglob("*.py"),
        *Path("./tests").glob("*.py"),
        *Path(".").glob("*.py"),
    ]

    for path in files:
        with open(path) as f:
            if "# Copyright (c)" not in f.readline():
                missing.append(path)

    if missing:
        session.error(
            "\nThe following files are missing their license:\n"
            + "\n".join(f" - {m}" for m in missing)
        )
