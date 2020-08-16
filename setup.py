import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fortecubeview-fevangelista",
    version="0.1.0",
    author="Francesco Evangelista",
    author_email="",
    description="A cube file viewer for Psi4 and Forte",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/evangelistalab/fortecubeview",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
