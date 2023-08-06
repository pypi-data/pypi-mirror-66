import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scraparser",
    version="0.0.2",
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
        "camelot-py>=0.7",
        "click>=7.1",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "opencv-python>=4.2",
        "python-magic>=0.4",
        "validators>=0.14.3",
    ],
    python_requires=">=3.6",
 )
