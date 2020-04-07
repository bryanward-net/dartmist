import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dartmist",
    version="0.0.1",
    author="Bryan Ward",
    author_email="bryan@bryanward.net",
    description="A library for interacting with the Mist Systems API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bryanward-net/dartmist",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GENERAL PUBLIC LICENSE V3 (GPLV3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)
