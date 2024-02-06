#!/usr/bin/env python3
from pathlib import Path

import setuptools
from setuptools import setup

module_name = "unicode_rbnf"
this_dir = Path(__file__).parent
module_dir = this_dir / module_name
data_files = list((module_dir / "rbnf").glob("*.xml"))

version_path = module_dir / "VERSION"
data_files.append(version_path)
version = version_path.read_text(encoding="utf-8").strip()

long_description = (this_dir / "README.md").read_text()

# -----------------------------------------------------------------------------

setup(
    name=module_name,
    version=version,
    description="Rule-based number formatting using Unicode CLDR data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/rhasspy/unicode-rbnf",
    author="Michael Hansen",
    author_email="mike@rhasspy.org",
    license="MIT",
    packages=setuptools.find_packages(),
    package_data={
        module_name: [str(p.relative_to(module_dir)) for p in data_files] + ["py.typed"]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="rbnf unicode number format",
)
