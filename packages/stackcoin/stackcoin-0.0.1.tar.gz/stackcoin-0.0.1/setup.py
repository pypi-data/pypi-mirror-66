import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

setuptools.setup(
    name="stackcoin",
    version="0.0.1",
    author="Jack Arthur Harrhy",
    author_email="me@jackharrhy.com",
    description="Python client for interacting with the StackCoin HTTP API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jackharrhy/stackcoin-python",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
