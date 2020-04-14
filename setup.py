import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="psi4cubeview-pkg", # Replace with your own username
    version="0.0.1",
    author="Francesco Evangelista",
    author_email="",
    description="A cube file viewer for Psi4",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/evangelistalab/psi4cubeview",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
