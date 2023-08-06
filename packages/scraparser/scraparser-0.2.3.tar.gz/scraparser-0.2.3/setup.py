import setuptools
import os, re, sys

with open("README.md", "r") as fh:
    long_description = fh.read()

long_description = re.sub(
    r'\[(.+?)\]\((?!(http|https):\/\/)(.+?)\)',
    r'[\1](https://gitlab.com/yookoala/scraparser/-/blob/master/\3)',
    long_description
)

name = os.getenv("PACKAGE_NAME")
if name is None:
    name = "scraparser"

version = os.getenv("VERSION")
if version is None:
    version = "0.1.0"

setuptools.setup(
    name=name,
    version=version,
    scripts=[],
    author="Koala Yeung",
    author_email="koalay@gmail.com",
    description="A simplified PDF table scraping and parsing tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/yookoala/scraparser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "camelot-py>=0.7"
        "click>=7.1"
        "google-api-python-client>=1.8"
        "google-auth-httplib2>=0.0.3"
        "google-auth-oauthlib>=0.4"
        "opencv-python>=4.2"
        "python-magic>=0.4"
        "validators>=0.14"
    ],
    python_requires=">=3.6",
 )
