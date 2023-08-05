import setuptools
from pathlib import Path

setuptools.setup(
    name = "kazopdf",
    version = 1.0,
    description = Path("README.md").read_text(),
    packages = setuptools.find_packages(exclude = ["tests", "data"])
)