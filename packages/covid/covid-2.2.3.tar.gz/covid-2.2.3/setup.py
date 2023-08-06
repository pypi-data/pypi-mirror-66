# -*- coding: utf-8 -*-
import io
import os
from setuptools import setup

with io.open("README.md") as f:
    long_description = f.read()

version = os.popen("git describe --abbrev=0 --tags").read()
version = version.strip().replace("v", "")

setup(
    name="covid",
    version=version,
    description="Python package to get information regarding the novel corona virus provided by Johns Hopkins university and worldometers.info",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ahmednafies.github.io/covid/",
    author="Ahmed Nafies",
    author_email="ahmed.nafies@gmail.com",
    license="MIT",
    packages=["covid", "covid.john_hopkins", "covid.worldometers"],
    install_requires=["requests", "pydantic", "beautifulsoup4"],
    extras_require={
        "dev": [
            "pipenv",
            "pytest",
            "coverage",
            "flake8",
            "ipdb",
            "pre-commit",
            "black",
        ],
        "docs": ["mkdocs", "mkdocs-material"],
    },
    project_urls={
        "Documentation": "https://ahmednafies.github.io/covid/",
        "Source": "https://github.com/ahmednafies/covid",
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    zip_safe=False,
    python_requires=">=3.6",
)
