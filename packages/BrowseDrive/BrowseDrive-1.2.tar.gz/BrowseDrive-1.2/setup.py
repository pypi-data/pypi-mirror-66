import setuptools
from pathlib import Path
setuptools.setup(
    name="BrowseDrive",
    version=1.2,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(),
    install_requires=['selenium>=3.141','requests>=2.23.0','bs4>=0.0.1']
)
