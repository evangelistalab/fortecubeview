# fortecubeview

A simple cube file viewer based on pythreejs.

![fortecubeview](extra/screenshot.png)

## Installation
Using pip:
```
pip install fortecubeview
```

## Dependencies
forte4cubeview requires [pythreejs](https://github.com/jupyter-widgets/pythreejs) and [scikit-image](https://github.com/scikit-image/scikit-image).

To install pythreejs via pip:
```
pip install pythreejs
```

To install pythreejs via conda:
```
conda install -c conda-forge pythreejs
conda install nodejs -c conda-forge --repodata-fn=repodata.json
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
Check out the example files in the `fortecubeview/examples` folder.
From jupyter, the following will load and display all the cube files contained in the currrent working directory
```
    import fortecubeview
    fortecubeview.plot()
```

