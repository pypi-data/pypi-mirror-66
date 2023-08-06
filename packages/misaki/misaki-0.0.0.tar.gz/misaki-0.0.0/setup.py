# encoding: utf-8
from setuptools import setup, find_packages

pkg = "misaki"
ver = "0.0.0"

with open(pkg + "/version.py", "wt") as h:
    h.write('__version__ = "{}"\n'.format(ver))

setup(
    name=pkg,
    version=ver,
    description=("Code formatter and linter management tool"),
    long_description=(
        "Misaki is like pre-commit, except it never ever "
        "auto-downloads or runs code off the Internet. It's up "
        "to *you* to install whatever linter/formatters you want to use."
    ),
    author="Eduard Christian Dumitrescu",
    author_email="eduard.c.dumitrescu@gmail.com",
    license="GPLv3",
    url="https://hydra.ecd.space/eduard/misaki/",
    packages=find_packages(),
    data_files=[("", ["LICENSE", "COPYRIGHT", "README.md"])],
    install_requires=["argh", "attrs", "cached_property"],
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries",
    ],
)
