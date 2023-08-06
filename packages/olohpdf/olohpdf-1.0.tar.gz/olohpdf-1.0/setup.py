import setuptools
from pathlib import Path

setuptools.setup(
    name="olohpdf",
    version="1.0",
    long_description=Path("READ.md").read_text(),
    packages=setuptools.find_packages(exclude=["test", "data"])
)
