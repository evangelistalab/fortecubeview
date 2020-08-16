# psi4cubeview

A simple cube file viewer based on pythreejs.

![psi4cubeview](lib/screenshot.png)

## Installation
Using pip:
```
pip install psi4cubeview
```

## Dependencies
psi4cubeview requires [pythreejs](https://github.com/jupyter-widgets/pythreejs).

To install pythreejs via pip:
```
pip install pythreejs
```
And then install the extension for jupyter notebooks
```
jupyter nbextension install --py --symlink --sys-prefix pythreejs
jupyter nbextension enable --py --sys-prefix pythreejs
```
Or for jupyter lab:
```
jupyter labextension install @jupyter-widgets/jupyterlab-manager 
jupyter labextension install jupyter-threejs
```

## Getting started
Check out the example files in the `psi4cubeview/examples` folder.
From jupyter, the following will load and display all the cube files contained in the currrent working directory
```
    import psi4cubeview
    psi4cubeview.plot()
```

