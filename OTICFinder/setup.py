"""Setup script for OTICFinder"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="OTICFinder",
    version="1.2.0",
    description="OTICFinder allows the cleaning of addresses and geopositioning in the metropolitan area of Bucaramanga.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Oficina-TIC-BGA/OTICFinder",
    author="Jefferson Rodríguez",
    author_email="jefferson.rc94@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["OTICFinder"],
    include_package_data=True,
    install_requires=[
        "importlib_resources", "typing"
    ],
    entry_points={"console_scripts": ["oticfinder=OTICFinder.__main__:main"]},
)