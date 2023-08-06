"""simplesim package details.
This module contains the package details for simplesim.
"""

import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="simplesim",
    version="1.0.0",
    author="Adam Morrissett",
    author_email="me@adamlm.com",
    description="A simple and generic framework for quickly and easily "
                "creating a simulation environment",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    keywords="simple generic simulation environment framework",
    url="https://github.com/MeelonUsk/simplesim",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.5',
)
