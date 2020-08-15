from .cube_viewer import *

def plot():
#path='.',
#         cubes=None,
#         scale=1.0,
#         font_size=16,
#         font_family='Helvetica',
#         width=400,
#         height=400,
#         show_text=True):
    """
    A simple widget for viewing cube files. Cube files are authomatically loaded from the current
    directory. Alternatively, the user can pass a path or a dictionary containing CubeFile objects

    Parameters
    ----------
    path : str
        The path used to load cube files (default = '.')
    cubes : dict
        A dictionary {'filename.cube' : CubeFile } containing the cube files to be plotted
    scale : float
        the scale factor used to make a molecule smaller or bigger (default = 1.0)
    font_size : int
        the font size (default = 16)
    font_family : str
        the font used to label the orbitals (default = Helvetica)
    width : int
        the width of the plot in pixels (default = 400)
    height : int
        the height of the plot in pixels (default = 400)
    show_text : bool
        show the name of the cube file under the plot? (default = True)
    """

    return CubeViewer()
