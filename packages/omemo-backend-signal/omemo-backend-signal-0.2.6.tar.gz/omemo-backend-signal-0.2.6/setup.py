from setuptools import setup, find_packages

import os
import sys

version_file_path = os.path.join(
	os.path.dirname(os.path.abspath(__file__)),
	"omemo_backend_signal",
	"version.py"
)

version = {}

try:
	execfile(version_file_path, version)
except:
	with open(version_file_path) as fp:
		exec(fp.read(), version)

with open("README.md") as f:
    long_description = f.read()

setup(
    name = "omemo-backend-signal",
    version = version["__version__"],
    description = "A backend for python-omemo offering compatibility with libsignal.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Syndace/python-omemo-backend-signal",
    author = "Tim Henkes",
    author_email = "me@syndace.dev",
    license = "GPLv3",
    packages = find_packages(),
    install_requires = [
        "X3DH>=0.5.9,<0.6",
        "DoubleRatchet>=0.7.0,<0.8",
        "OMEMO>=0.11.0,<0.13",
        "cryptography>=1.7.1",
        "protobuf>=2.6.1"
    ],
    python_requires = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4",
    zip_safe = False,
    classifiers = [
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "Topic :: Communications :: Chat",
        "Topic :: Security :: Cryptography",

        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",

        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ]
)
