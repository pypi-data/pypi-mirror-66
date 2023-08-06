from setuptools import setup, find_packages

setup(
    name="pretermgrowth",
    version="0.1",
    packages=find_packages(),
    # metadata to display on PyPI
    author="Matt Devine",
    author_email="mddevine@gmail.com",
    description="Calculate growth measurement z-scores for preterm infants",
    keywords="preterm neonatology fenton growth",
    project_urls={"Source Code": "https://github.com/gammaflauge/pretermgrowth/"},
    download_url="https://github.com/gammaflauge/pretermgrowth/archive/0.1.tar.gz",
)
