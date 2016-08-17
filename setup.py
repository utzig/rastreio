import os
from setuptools import setup

setup(
    name = "rastreio",
    version = "0.0.2",
    author = "Fabio Utzig",
    author_email = "utzig@utzig.org",
    description = ("Utility to track packages in the Brazilian post site"),
    license = "MIT",
    url = "http://github.com/utzig/rastreio",
    packages=["rastreio"],
    scripts=["rastreio/rastreio.py"],
    entry_points = {
        "console_scripts": [ "rastreio = rastreio:main" ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
