#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time

import ipywidgets as widgets
from .py3js_renderer import Py3JSRenderer

#def list_cubes(path='.'):
#    """
#    List all the cubefiles (suffix ".cube" ) in a given path

#    Parameters
#    ----------
#    path : str
#        The path of the directory that will contain the cube files
#    """

#    import os
#    cube_files = []
#    isdir = os.path.isdir(path)
#    if isdir:
#        for file in os.listdir(path):
#            if file.endswith('.cube'):
#                cube_files.append(os.path.join(path, file))
#        if len(cube_files) == 0:
#            print(f'load_cubes: no cube files found in directory {path}')
#    else:
#        print(f'load_cubes: directory {path} does not exist')

#    return cube_files



class VibViewer():
    """
    A simple widget for visualizing normal modes. Molden normal modes are loaded from the current
    directory. Alternatively, the user can pass the name of the file

    Parameters
    ----------
    file : str
        The normal mode file
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
    show_text : bool
        show the name of the cube file under the plot? (default = True)
    """
    def __init__(self,
                 file = None,
                 path = '.',
                 width=400,
                 height=400,
                 font_size=16,
                 font_family='Helvetica',
                 show_text=True):

        start_time = time.perf_counter()

        if file == None:
            print(f'VibViewer: loading normal mode file from the current directory {path}')

        self.debug = False
        self.file = file
        self.path = path
        self.width = width
        self.height = height
        self.scale = 1.0
        self.font_size = font_size
        self.font_family = font_family
        self.show_text = show_text

        data = self.parse_normal_modes_file()

        box_layout = widgets.Layout(border='0px solid black',
                                    width=f'{width + 50}px',
                                    height=f'{height + 100}px')

#        # start a CubeLoader
#        cube_loader = CubeLoader(cubes=cubes)
        # start a Py3JSRenderer
        renderer = Py3JSRenderer(width=width, height=height)

        make_objs_time = time.perf_counter()

        if self.debug:
            print(f'Time to make objects: {make_objs_time-start_time}')

        make_meshes_time = time.perf_counter()

        # add molecule to the renderer
        renderer.add_molecule(data['coords'],bohr=True, shift_to_com=False)
        renderer.add_normal_modes(data['frequencies'],data['modes'])

        sorted_labels = []
        for k, freq in enumerate(data['frequencies']):
            if freq < 0.0:
                str = f"i{-freq:6.1f}"
            else:
                str = f" {freq:6.1f}"
            sorted_labels.append(f'Normal mode {k + 1} ({str} cm^-1)')
        labels_to_modes = {}
        for k, label in enumerate(sorted_labels):
            labels_to_modes[label] = k

#        first = True
#        for label in sorted_labels:
#            filename = labels_to_filename[label]
#            cube = cube_loader.load(filename)
#            type = 'density' if label[0] == 'D' else 'mo'
#            renderer.add_cubefiles(cube,
#                                   type=type,
#                                   colorscheme=colorscheme,
#                                   levels=levels,
#                                   colors=colors,
#                                   opacity=opacity,
#                                   sumlevel=sumlevel,
#                                   add_geom=first)
#            if first: first = False

        style = f'font-size:{font_size}px;font-family:{font_family};font-weight: bold;'
        mo_label = widgets.HTML()
        file_label = widgets.HTML()

        def update_renderer(label, objects):
            """This function updates the rendeder once the user has selected a new mode to plot"""
            start_update_time = time.perf_counter()

            renderer, style, labels_to_modes = objects
            mode = labels_to_modes[label]

#            # update the renderer
#            renderer.set_active_mode(mode)

            # update the labels
            file_label.value = f'<div align="center">({mode})</div>'
            mo_label.value = f'<div align="center" style="{style}">{label}</div>'

            end_update_time = time.perf_counter()
            if self.debug:
                print(
                    f'Time to update objects ({label}): {end_update_time-start_update_time}'
                )

        ws = widgets.Select(options=sorted_labels, description='Cube files:')
        interactive_widget = widgets.interactive(update_renderer,
                                                 label=ws,
                                                 objects=widgets.fixed(
                                                     (renderer, style,
                                                      labels_to_modes)))

        output = interactive_widget.children[-1]
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
        display(
            widgets.VBox([mo_label, renderer.renderer, file_label],
                         layout=box_layout))

        # disable scroll and display the selection widget
        display(widgets.HTML(widget_style))
        display(interactive_widget)
        display_time = time.perf_counter()
        if self.debug:
            print(f'Time to prepare renderer: {display_time-start_time}')


    def parse_normal_modes_file(self):
        # convert normal modes into human readable text
        labels_to_modes = {}
        data = {'frequencies' : [],'coords' : [],'modes' : []}

        with open(self.file,'r') as f:
            lines = f.readlines()
            for line in lines[3:]:
                if line.strip() == '':
                    break
                else:
                    data['frequencies'].append(float(line))
            num_freq = len(data['frequencies'])
            for line in lines[5 + num_freq:]:
                if line.strip() == '':
                    break
                else:
                    sline = line.split()
                    data['coords'].append((sline[0],float(sline[1]),float(sline[2]),float(sline[3])))
            num_atoms = len(data['coords'])
            for n in range(num_freq):
                mode = []
                start = 8 + num_freq + num_atoms + n * (num_atoms + 1)
                end = 8 + num_freq + 2 * num_atoms + n * (num_atoms + 1)
                for line in lines[start:end]:
                    mode.append([float(s) for s in line.split()])
                data['modes'].append(mode)

        return data
