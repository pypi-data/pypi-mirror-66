import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="alfred3_dbtools",
    version="0.1.0",
    author="Christian Treffenstädt, Johannes Brachem",
    author_email="treffenstaedt@psych.uni-goettingen.de",
    description="A package that provides tools for interacting with databases when working with alfred3 experiments.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ctreffe/alfred3-dbtools",
    packages=setuptools.find_packages(),
    install_requires=["alfred>=1.0.0", "pymongo>=3.10"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)