from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="d-utils",
    version="0.0.3",
    author="Johannes Velde",
    author_email="johannes.velde@gmx.de",
    description="Utilities for Web Scraping",
    py_modules=["webdriverutils", "browser-utils"],
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,  # README.md
    long_description_content_type="text/markdown",
    install_requires=[
        "selenium", 'pyvirtualdisplay',
    ],
    ##FOR Development pruposes only
    extras_require={
        "dev": [
            "pytest>=3.7",
        ],
    },
)
