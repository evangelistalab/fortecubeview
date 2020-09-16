#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time

import ipywidgets as widgets
from .py3js_renderer import Py3JSRenderer

class MolViewer():
    """
    A simple widget for visualizing normal modes. Molden normal modes are loaded from the current
    directory. Alternatively, the user can pass the name of the file

    Parameters
    ----------
    filename : str
        The name of a molden normal mode file
    width : int
        the width of the plot in pixels (default = 400)
    height : int
        the height of the plot in pixels (default = 400)
    scale : float
        the scale factor used to make a molecule smaller or bigger (default = 1.0)
    font_size : int
        the font size (default = 16)
    font_family : str
        the font used to label the orbitals (default = Helvetica)
    """
    def __init__(self,
                 xyz = None,
                 molecule = None,
                 path = '.',
                 width=400,
                 height=400,
                 font_size=16,
                 font_family='Helvetica'):


        if xyz == None and molecule == None:
            print(
                f'MolViewer: no molecule provided. The widget will not be displayed'
            )
            return

        geom = []

        if molecule != None:
            xyz = '\n'.join(molecule.to_string(dtype='xyz').split('\n')[2:])

        if xyz != None:
            for line in xyz.split('\n'):
                sline = line.split()
                if len(sline) > 0:
                    if not sline[0].isnumeric():
                        geom.append((sline[0],float(sline[1]),float(sline[2]),float(sline[3])))

        # start a Py3JSRenderer
        renderer = Py3JSRenderer(width=width, height=height)

        # add molecule to the renderer
        renderer.add_molecule(geom,bohr=False, shift_to_com=False)

        # output.layout.height = f'{height + 100}px'
        widget_style = """
        <style>
           .jupyter-widgets-output-area .output_scroll {
                height: unset !important;
                border-radius: unset !important;
                -webkit-box-shadow: unset !important;
              box-shadow: unset !important;
            }
            .jupyter-widgets-output-area  {
            height: auto !important;
         }
        </style>
        """

        # display the rendered and the labels
        display(renderer.renderer)

        # disable scroll and display the selection widget
#        display(widgets.HTML(widget_style))
