import setuptools
from pathlib import Path

setuptools.setup(
    name="mjhello",
    version=1.0,
    long_description=Path("README.md").read_text(),
    package=setuptools.find_packages(exclude=["data", "test"])

)
