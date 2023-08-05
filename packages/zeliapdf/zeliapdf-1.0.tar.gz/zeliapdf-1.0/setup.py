import setuptools
from pathlib import Path

setuptools.setup(
    name="zeliapdf",
    version=1.0,
    long_descripton=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"]),
    setup_requires=['wheel']
)
