from setuptools import setup, find_packages
from codecs import open
from os import path
import sys


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="lcdchargen",
    version="0.1",
    author="S.V. Matsievskiy",
    author_email="matsievskiysv@gmail.com",
    maintainer="S.V. Matsievskiy",
    maintainer_email="matsievskiysv@gmail.com",
    url="https://gitlab.com/matsievskiysv/lcdchargen",
    description="Generate custom character for HD44780U LCD screen",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3+",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: GTK",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Embedded Systems",
    ],
    keywords="LCD display HD44780U",
    include_package_data=True,
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    install_requires=["pycairo", "PyGObject"],
    python_requires='>=3.5',
    entry_points={"console_scripts": ["lcdchargen = lcdchargen.lcdchargen:main"]},
)
