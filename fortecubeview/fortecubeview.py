from .cube_viewer import *
from .vib_viewer import *
from .mol_viewer import *

# The allowed color schemes
colorschemes = ['emory', 'national', 'bright', 'electron', 'wow']

def geom(xyz = None,
         molecule = None,
         width=400,
         height=400):
    """
    A simple widget for render a psi4 molecule object.

    Parameters
    ----------
    xyz : Molecule
        A psi4 Molecule object to render
    width : int
        the width of the plot in pixels (default = 400)
    height : int
        the height of the plot in pixels (default = 400)
    """
    return MolViewer(
        xyz=xyz,
        molecule=molecule,
        width=width,
        height=height,
    )

def plot(path='.',
         cubes=None,
         width=400,
         height=400,
         colorscheme='emory',
         levels=None,
         colors=None,
         opacity=1.0,
         sumlevel=0.85,
         show_text=True,
         font_size=16,
         font_family='Helvetica'):
    """
    A simple widget for viewing cube files. Cube files are authomatically loaded from the current
    directory. Alternatively, the user can pass a path or a dictionary containing CubeFile objects

    Parameters
    ----------
    path : str
        The path used to load cube files (default = '.')
    cubes : list
        List of cube files to be plotted
    width : int
        the width of the plot in pixels (default = 400)
    height : int
        the height of the plot in pixels (default = 400)
    colorscheme : str
        the colors scheme used to represent the orbitals/densities.
        Options include emory (default), national, bright, electron, wow
    levels : list(float)
        a list of levels to plot (default = None).
        Overrides the colorscheme option and must be defined together with the option colors
    colors: list(hexadecimal colors)
        a list of colors for the levels. E.g. ['#f2a900'] (default = None)
    opacity: float [0-1]
        the opacity of the surfaces (default = 1.0)
    sumlevel: float [0-1]
        the fraction of the electron density used to determine the countour levels (default = 0.75)
    font_size : int
        the font size (default = 16)
    font_family : str
        the font used to label the orbitals (default = Helvetica)
    show_text : bool
        show the name of the cube file under the plot? (default = True)
    """
    return CubeViewer(
        cubes=cubes,
        path=path,
        width=width,
        height=height,
        colorscheme=colorscheme,
        levels=levels,
        colors=colors,
        font_size=font_size,
        font_family=font_family,
        opacity=opacity,
        sumlevel=sumlevel,
    )

def vib(filename,
        path='.',
        width=400,
        height=400,
        show_text=True,
        font_size=16,
        font_family='Helvetica'):
    """
    A simple widget for viewing cube files. Cube files are authomatically loaded from the current
    directory. Alternatively, the user can pass a path or a dictionary containing CubeFile objects

    Parameters
    ----------
    path : str
        The path used to load cube files (default = '.')
    cubes : list
        List of cube files to be plotted
    width : int
        the width of the plot in pixels (default = 400)
    height : int
        the height of the plot in pixels (default = 400)
    colorscheme : str
        the colors scheme used to represent the orbitals/densities.
        Options include emory (default), national, bright, electron, wow
    levels : list(float)
        a list of levels to plot (default = None).
        Overrides the colorscheme option and must be defined together with the option colors
    colors: list(hexadecimal colors)
        a list of colors for the levels. E.g. ['#f2a900'] (default = None)
    opacity: float [0-1]
        the opacity of the surfaces (default = 1.0)
    sumlevel: float [0-1]
        the fraction of the electron density used to determine the countour levels (default = 0.75)
    font_size : int
        the font size (default = 16)
    font_family : str
        the font used to label the orbitals (default = Helvetica)
    show_text : bool
        show the name of the cube file under the plot? (default = True)
    """
    return VibViewer(
        filename=filename,
        path=path,
        width=width,
        height=height,
        font_size=font_size,
        font_family=font_family,
    )
