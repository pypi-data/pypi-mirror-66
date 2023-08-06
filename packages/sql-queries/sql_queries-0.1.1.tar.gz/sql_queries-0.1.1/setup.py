import setuptools
from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sql_queries",
    version="0.1.1",
    author="Simon van Meegdenburg",
    author_email="simonvm@live.nl",
    description="Build simple SQL queries fast and clean",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    projectURLs={
        "Source code": "https://github.com/Simonvm9114/sql_queries",
        "Youtube": "https://www.youtube.com/playlist?list=PLI4WFrsrAg8sCeBj5xdJ6n79_3Yq3Sz23"
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: SQL",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Topic :: Database"
    ],
    python_requires='>=3.6',
    setup_requires=['wheel']
)
