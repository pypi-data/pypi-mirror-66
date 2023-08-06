import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simply-giphy-cli-nronnei",
    version="0.0.2",
    author="Nick Ronnei",
    author_email="nronnei@gmail.com",
    description="A simple python-based CLI for searching Giphy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
