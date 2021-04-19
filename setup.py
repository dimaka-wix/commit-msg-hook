from setuptools import setup, find_packages

# Load the README file.
with open(file="README.md", mode="r") as readme_handle:
    README = readme_handle.read()

setup(
    # The name that used along with `pip install`
    name="commit-msg-hook",
    author="Dima Karpukhin",
    author_email="dimadk787@gmail.com",
    version="0.1.0",

    # The description that appears when someone searches for the library on https://pypi.org/search
    description="Checks if commit message matches the chaos-hub commit rules",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/DimaKarpukhin/commit-msg-hook.git",


    # The packages I want "build."
    packages=find_packages(),
)
