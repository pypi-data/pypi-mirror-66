import os

import setuptools

from smokeur.cli import VERSION


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

package_requirements = [
    "bump2version",
    "setuptools",
    "wheel",
    "twine",
]

setuptools.setup(
    name="smokeur cli",
    version=VERSION,
    license="BSD",
    description="Smokeur client for CLI.",
    long_description=read("README.rst"),
    author="c0x6a",
    author_email="cj@carlosjoel.net",
    url="https://gitlab.com/c0x6a/smokeur-cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    zip_safe=False,
    extras_require={"package": package_requirements},
    install_requires=["requests", "pyperclip", "click"],
    entry_points={"console_scripts": ["smokeur=smokeur.cli:cli"]},
)
