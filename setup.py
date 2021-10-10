import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gamesense",
    version="0.0.5",
    author="Casey Richardson",
    author_email="caseybrichardson@icloud.com",
    description="Library for interacting with SteelSeries GameSense 3.8.x",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/caseybrichardson/gamesense",
    packages=setuptools.find_packages(),
    extras_require={
        "sync": ["requests"],
        "async": ["aiohttp"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
