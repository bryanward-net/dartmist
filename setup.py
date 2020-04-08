import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dartmist",
    version="0.0.7",
    author="Bryan Ward",
    author_email="bryan@bryanward.net",
    description="A library for interacting with the Mist Systems API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.bryanward.net/dartmist",
    project_urls={
        'Homepage': 'https://www.bryanward.net/dartmist',
        'Source': 'https://github.com/bryanward-net/dartmist'
    },
    packages=["dartmist"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['websocket', 'websocket-client'],
    keywords='mist api wifi wi-fi juniper'
)
