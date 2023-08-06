import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simply-giphy-cli-nronnei",
    version="0.0.5",
    author="Nick Ronnei",
    author_email="nronnei@gmail.com",
    description="A simple python-based CLI for searching Giphy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "certifi==2020.4.5.1",
        "giphy-client==1.0.0",
        "pyperclip==1.8.0",
        "python-dateutil==2.8.1",
        "six==1.14.0",
        "urllib3==1.25.9"
    ],
    python_requires='>=3.6',
)
