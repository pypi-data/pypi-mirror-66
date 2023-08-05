import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crypno",
    version="1.0.0",
    author="Crypno Co",
    author_email="crypnoco@gmail.com",
    description="Crypno Python Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://crypno.ir",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)