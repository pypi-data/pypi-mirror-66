import pathlib
from setuptools import setup
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
    name="quantbacktest",
    version="0.0.1",
    description="",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Jan Frederic Spörer",
    author_email="jan.spoerer@whu.edu",
    license="BSD two-clause license",
    packages=["quantbacktest"],
    install_requires=["sys", "os", "copy", "math", "datetime", "random", "numpy", "matplotlib", "pandas"],
    url="https://gitlab.com/fsbc/theses/quantbacktest",
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "FullBacktest=quantbacktest.__main__:main",
        ]
    },
    include_package_data=True,
) # Source of this setup.py: Jonathan Hsu
# https://medium.com/better-programming/how-to-publish-your-first-python-package-its-not-that-hard-6202f74f5954
