"""
pyexos - Extreme Networks Config Manipulation
Copyright (C) 2020 Internet Association of Australian (IAA)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import setuptools

from pyexos import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ixau-pyexos",
    version=__version__,
    author="Nick Pratley",
    author_email="nick@ix.asn.au",
    description="pyexos - An Extreme Networks config manipulation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ixaustralia/pyexos",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires="~=3.5",
    install_requires=["netmiko"],
)
