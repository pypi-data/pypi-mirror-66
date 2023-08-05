import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BrowseDrive",
    version=1.7,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['selenium>=3.141','requests>=2.23.0','bs4>=0.0.1']
)
