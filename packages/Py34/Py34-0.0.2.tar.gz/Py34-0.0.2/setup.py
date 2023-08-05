import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Py34",
    version="0.0.2",
    author="Wallkker",
    author_email="",
    description="A simple API to retrieve data from Rule34.xxx",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Wallkker/Py34API",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)