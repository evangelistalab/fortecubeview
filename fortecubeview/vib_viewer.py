#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time

import ipywidgets as widgets
from .py3js_renderer import Py3JSRenderer

class VibViewer():
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
                 filename = None,
                 path = '.',
                 width=400,
                 height=400,
                 font_size=16,
                 font_family='Helvetica'):

        start_time = time.perf_counter()

        if filename == None:
            print(f'VibViewer: loading normal mode file from the current directory {path}')

        self.debug = False
        self.filename = filename
        self.path = path
        self.width = width
        self.height = height
        self.scale = 1.0
        self.font_size = font_size
        self.font_family = font_family

        data = self.parse_normal_modes_file()

        box_layout = widgets.Layout(border='0px solid black',
                                    width=f'{width + 50}px',
                                    height=f'{height + 50}px')

        # start a Py3JSRenderer
        renderer = Py3JSRenderer(width=width, height=height)

        make_objs_time = time.perf_counter()

        if self.debug:
            print(f'Time to make objects: {make_objs_time-start_time}')

        make_meshes_time = time.perf_counter()

        # add molecule to the renderer
        renderer.add_molecule(data['coords'],bohr=True, shift_to_com=False)
        renderer.add_normal_modes(data['coords'],data['frequencies'],data['modes'])

        sorted_labels = []
        for k, freq in enumerate(data['frequencies']):
            if freq < -25.0:
                str = f"{k + 1}: Imaginary mode (i{-freq:.1f} cm^-1)"
            elif -25.0 <= freq < 0.0:
                str = f"{k + 1}: Near-zero imaginary mode (i{-freq:.1f} cm^-1)"
            elif 0.0 <= freq < 50.0:
                str = f"{k + 1}: Near-zero normal mode ({freq:.1f} cm^-1)"
            else:
                str = f"{k + 1}: Normal mode ({freq:.1f} cm^-1)"
            sorted_labels.append(str)
        labels_to_modes = {}
        for k, label in enumerate(sorted_labels):
            labels_to_modes[label] = k

        style = f'font-size:{font_size}px;font-family:{font_family};font-weight: bold;'
        mo_label = widgets.HTML()

        def update_renderer(label, objects):
            """This function updates the rendeder once the user has selected a new mode to plot"""
            start_update_time = time.perf_counter()

            renderer, style, labels_to_modes = objects
            mode = labels_to_modes[label]

            # update the renderer
            renderer.set_active_mode(mode)

            # update the labels
            mo_label.value = f'<div align="center" style="{style}">{label}</div>'

            end_update_time = time.perf_counter()
            if self.debug:
                print(
                    f'Time to update objects ({label}): {end_update_time-start_update_time}'
                )

        ws = widgets.Select(options=sorted_labels, description='Select:')
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
            widgets.VBox([mo_label, renderer.renderer],
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

        with open(self.filename,'r') as f:
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
