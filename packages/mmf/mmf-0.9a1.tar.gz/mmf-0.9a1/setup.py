#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
import os.path
import re
import shutil
import sys
from glob import glob

import setuptools
from setuptools import Extension
from setuptools.command.build_ext import build_ext

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "mmf"))


def clean_html(raw_html):
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", raw_html).strip()
    return cleantext


with open("README.md", encoding="utf8") as f:
    readme = f.read()
    # https://stackoverflow.com/a/12982689
    readme = clean_html(readme)

with open("requirements.txt") as f:
    reqs = f.read()

DISTNAME = "mmf"
DESCRIPTION = "mmf: a modular framework for vision and language multimodal \
research."
LONG_DESCRIPTION = readme
LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"
AUTHOR = "Facebook AI Research"
AUTHOR_EMAIL = "mmf@fb.com"
REQUIREMENTS = (reqs.strip().split("\n"),)
VERSION = "0.9.alpha1"

ext_modules = [
    Extension(
        "cphoc",
        sources=["mmf/utils/phoc/src/cphoc.c"],
        language="c",
        libraries=["pthread", "dl", "util", "rt", "m"],
        extra_compile_args=["-O3"],
    )
]


class BuildExt(build_ext):
    def run(self):
        build_ext.run(self)
        cphoc_lib = glob("build/lib.*/cphoc.*.so")[0]
        shutil.copy(cphoc_lib, "mmf/utils/phoc/cphoc.so")


if __name__ == "__main__":
    setuptools.setup(
        name=DISTNAME,
        install_requires=REQUIREMENTS,
        packages=setuptools.find_packages(),
        ext_modules=ext_modules,
        cmdclass={"build_ext": BuildExt},
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        setup_requires=["pytest-runner"],
        tests_require=["flake8", "pytest"],
    )
