from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pretermgrowth",
    version="0.2",
    packages=find_packages(),
    # metadata to display on PyPI
    author="Matt Devine",
    author_email="mddevine@gmail.com",
    description="Calculate growth measurement z-scores for preterm infants",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="preterm neonatology fenton growth",
    project_urls={"Source Code": "https://github.com/gammaflauge/pretermgrowth/"},
    download_url="https://github.com/gammaflauge/pretermgrowth/archive/0.2.tar.gz",
    python_requires=">=3.6",
)
