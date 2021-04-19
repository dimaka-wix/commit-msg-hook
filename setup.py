from setuptools import setup, find_packages


setup(
    # The name that used along with `pip install`
    name="commit-msg-hook",
    author="Dima Karpukhin",
    author_email="dimadk787@gmail.com",
    version="0.1.0",

    # The description that appears on https://pypi.org/search
    description="Checks if commit message matches the chaos-hub commit rules",
    url="https://github.com/DimaKarpukhin/commit-msg-hook.git",

    # The packages I want "build."
    packages=find_packages(),
)
