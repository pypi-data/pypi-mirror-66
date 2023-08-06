"""setup for PyPI deploy
"""

from setuptools import find_packages, setup

VERSION = "0.0.1"  # update VERSION in constants.py
AUTHOR = "Predictive Healthcare @ Penn Medicine"
MAINTAINER = "Brian Ross, Code for Philly"
MAINTAINER_EMAIL = "ml@brianthomasross.com"
URL = "https://codeforphilly.github.io/chime/"
PROJECT_URLS={
    "Bug Reports": "https://github.com/CodeForPhilly/chime/issues",
    "Source": "https://github.com/CodeForPhilly/chime",
    "Documentation": "https://codeforphilly.github.io/chime/",
}
REQUIREMENTS = [
            "altair",
            "gspread",
            "numpy",
            "pandas",
            "pytest",
            "streamlit",
            "gspread",
            "oauth2client"
]
with open("README.rst", "r") as f:
    README = f.read()
CLASSIFIERS = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]


setup(
    name="penn-chime",
    version=VERSION,
    author=AUTHOR,
    author_email="",
    description="Covid-19 Hospital Impact Model for Epidemics",
    long_description=README,
    url=URL,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    test_suite='tests',

    python_requires='>=3.6.9',
    entry_points={
        'console_scripts': ['penn_chime=penn_chime.cli:main'],
    },
    include_package_data=True,
)












"""Setup file for chime
"""
__version__ = "1.1.3"  # update VERSION in constants.py
__author__ = "Predictive Healthcare @ Penn Medicine"

from setuptools import setup, find_namespace_packages



