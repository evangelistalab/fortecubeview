import numpy as np
import re
import functools 
import ipywidgets as widgets
import re
import math
import collections
import skimage.measure

from IPython.display import display
from pythreejs import *

"""
    A map from atom symbols to atomic number
"""
ATOM_SYMBOL_TO_Z = {
    'Xx': 0,
    'H': 1,
    'He': 2,
    'Li': 3,
    'Be': 4,
    'B': 5,
    'C': 6,
    'N': 7,
    'O': 8,
    'F': 9,
    'Ne': 10,
    'Na': 11,
    'Mg': 12,
    'Al': 13,
    'Si': 14,
    'P': 15,
    'S': 16,
    'Cl': 17,
    'Ar': 18,
    'K': 19,
    'Ca': 20,
    'Sc': 21,
    'Ti': 22,
    'V': 23,
    'Cr': 24,
    'Mn': 25,
    'Fe': 26,
    'Co': 27,
    'Ni': 28,
    'Cu': 29,
    'Zn': 30,
    'Ga': 31,
    'Ge': 32,
    'As': 33,
    'Se': 34,
    'Br': 35,
    'Kr': 36,
    'Rb': 37,
    'Sr': 38,
    'Y': 39,
    'Zr': 40,
    'Nb': 41,
    'Mo': 42,
    'Tc': 43,
    'Ru': 44,
    'Rh': 45,
    'Pd': 46,
    'Ag': 47,
    'Cd': 48,
    'In': 49,
    'Sn': 50,
    'Sb': 51,
    'Te': 52,
    'I': 53,
    'Xe': 54,
    'Cs': 55,
    'Ba': 56,
    'La': 57,
    'Ce': 58,
    'Pr': 59,
    'Nd': 60,
    'Pm': 61,
    'Sm': 62,
    'Eu': 63,
    'Gd': 64,
    'Tb': 65,
    'Dy': 66,
    'Ho': 67,
    'Er': 68,
    'Tm': 69,
    'Yb': 70,
    'Lu': 71,
    'Hf': 72,
    'Ta': 73,
    'W': 74,
    'Re': 75,
    'Os': 76,
    'Ir': 77,
    'Pt': 78,
    'Au': 79,
    'Hg': 80,
    'Tl': 81,
    'Pb': 82,
    'Bi': 83,
    'Po': 84,
    'At': 85,
    'Rn': 86,
    'Fr': 87,
    'Ra': 88,
    'Ac': 89,
    'Th': 90,
    'Pa': 91,
    'U': 92,
    'Np': 93,
    'Pu': 94,
    'Am': 95,
    'Cm': 96,
    'Bk': 97,
    'Cf': 98,
    'Es': 99,
    'Fm': 100
}
"""
    A map from atom symbols to atomic data
"""
ATOM_DATA = [{
    'symbol': 'Xx',
    'name': 'Dummy',
    'mass': 0,
    'radius_covalent': 0.18,
    'radius_VDW': 0.69,
    'color': [17, 127, 178]
}, {
    'symbol': 'H',
    'name': 'Hydrogen',
    'mass': 1.00784,
    'radius_covalent': 0.32,
    'radius_VDW': 1.2,
    'color': [240, 240, 240]
}, {
    'symbol': 'He',
    'name': 'Helium',
    'mass': 4.0026,
    'radius_covalent': 0.46,
    'radius_VDW': 1.43,
    'color': [217, 255, 255]
}, {
    'symbol': 'Li',
    'name': 'Lithium',
    'mass': 6.938,
    'radius_covalent': 1.33,
    'radius_VDW': 2.12,
    'color': [204, 128, 255]
}, {
    'symbol': 'Be',
    'name': 'Beryllium',
    'mass': 9.01218,
    'radius_covalent': 1.02,
    'radius_VDW': 1.98,
    'color': [194, 255, 0]
}, {
    'symbol': 'B',
    'name': 'Boron',
    'mass': 10.806,
    'radius_covalent': 0.85,
    'radius_VDW': 1.91,
    'color': [255, 181, 181]
}, {
    'symbol': 'C',
    'name': 'Carbon',
    'mass': 12.011,
    'radius_covalent': 0.75,
    'radius_VDW': 1.77,
    'color': [127, 127, 127]
}, {
    'symbol': 'N',
    'name': 'Nitrogen',
    'mass': 14.006,
    'radius_covalent': 0.71,
    'radius_VDW': 1.66,
    'color': [48, 80, 255]
}, {
    'symbol': 'O',
    'name': 'Oxygen',
    'mass': 15.9994,
    'radius_covalent': 0.63,
    'radius_VDW': 1.5,
    'color': [200, 13, 13]
}, {
    'symbol': 'F',
    'name': 'Fluorine',
    'mass': 18.9984,
    'radius_covalent': 0.64,
    'radius_VDW': 1.46,
    'color': [178, 255, 255]
}, {
    'symbol': 'Ne',
    'name': 'Neon',
    'mass': 20.1797,
    'radius_covalent': 0.67,
    'radius_VDW': 1.58,
    'color': [178, 227, 245]
}, {
    'symbol': 'Na',
    'name': 'Sodium',
    'mass': 22.9898,
    'radius_covalent': 1.55,
    'radius_VDW': 2.5,
    'color': [171, 91, 242]
}, {
    'symbol': 'Mg',
    'name': 'Magnesium',
    'mass': 24.305,
    'radius_covalent': 1.39,
    'radius_VDW': 2.51,
    'color': [138, 255, 0]
}, {
    'symbol': 'Al',
    'name': 'Aluminium',
    'mass': 26.9815,
    'radius_covalent': 1.26,
    'radius_VDW': 2.25,
    'color': [191, 166, 166]
}, {
    'symbol': 'Si',
    'name': 'Silicon',
    'mass': 28.0855,
    'radius_covalent': 1.16,
    'radius_VDW': 2.19,
    'color': [240, 200, 160]
}, {
    'symbol': 'P',
    'name': 'Phosphorus',
    'mass': 30.9738,
    'radius_covalent': 1.11,
    'radius_VDW': 1.9,
    'color': [255, 128, 0]
}, {
    'symbol': 'S',
    'name': 'Sulfur',
    'mass': 32.065,
    'radius_covalent': 1.03,
    'radius_VDW': 1.89,
    'color': [255, 255, 48]
}, {
    'symbol': 'Cl',
    'name': 'Chlorine',
    'mass': 35.453,
    'radius_covalent': 0.99,
    'radius_VDW': 1.82,
    'color': [31, 240, 31]
}, {
    'symbol': 'Ar',
    'name': 'Argon',
    'mass': 39.948,
    'radius_covalent': 0.96,
    'radius_VDW': 1.83,
    'color': [128, 209, 227]
}, {
    'symbol': 'K',
    'name': 'Potassium',
    'mass': 39.0983,
    'radius_covalent': 1.96,
    'radius_VDW': 2.73,
    'color': [143, 64, 212]
}, {
    'symbol': 'Ca',
    'name': 'Calcium',
    'mass': 40.078,
    'radius_covalent': 1.71,
    'radius_VDW': 2.62,
    'color': [61, 255, 0]
}, {
    'symbol': 'Sc',
    'name': 'Scandium',
    'mass': 44.9559,
    'radius_covalent': 1.48,
    'radius_VDW': 2.58,
    'color': [230, 230, 230]
}, {
    'symbol': 'Ti',
    'name': 'Titanium',
    'mass': 47.867,
    'radius_covalent': 1.36,
    'radius_VDW': 2.46,
    'color': [191, 194, 199]
}, {
    'symbol': 'V',
    'name': 'Vanadium',
    'mass': 50.9415,
    'radius_covalent': 1.34,
    'radius_VDW': 2.42,
    'color': [166, 166, 171]
}, {
    'symbol': 'Cr',
    'name': 'Chromium',
    'mass': 51.9961,
    'radius_covalent': 1.22,
    'radius_VDW': 2.45,
    'color': [138, 153, 199]
}, {
    'symbol': 'Mn',
    'name': 'Manganese',
    'mass': 54.938,
    'radius_covalent': 1.19,
    'radius_VDW': 2.45,
    'color': [156, 122, 199]
}, {
    'symbol': 'Fe',
    'name': 'Iron',
    'mass': 55.845,
    'radius_covalent': 1.16,
    'radius_VDW': 2.44,
    'color': [224, 102, 51]
}, {
    'symbol': 'Co',
    'name': 'Cobalt',
    'mass': 58.9332,
    'radius_covalent': 1.11,
    'radius_VDW': 2.4,
    'color': [240, 144, 160]
}, {
    'symbol': 'Ni',
    'name': 'Nickel',
    'mass': 58.6934,
    'radius_covalent': 1.1,
    'radius_VDW': 2.4,
    'color': [80, 208, 80]
}, {
    'symbol': 'Cu',
    'name': 'Copper',
    'mass': 63.546,
    'radius_covalent': 1.12,
    'radius_VDW': 2.38,
    'color': [200, 128, 51]
}, {
    'symbol': 'Zn',
    'name': 'Zinc',
    'mass': 65.38,
    'radius_covalent': 1.18,
    'radius_VDW': 2.39,
    'color': [125, 128, 176]
}, {
    'symbol': 'Ga',
    'name': 'Gallium',
    'mass': 69.723,
    'radius_covalent': 1.24,
    'radius_VDW': 2.32,
    'color': [194, 143, 143]
}, {
    'symbol': 'Ge',
    'name': 'Germanium',
    'mass': 72.64,
    'radius_covalent': 1.21,
    'radius_VDW': 2.29,
    'color': [102, 143, 143]
}, {
    'symbol': 'As',
    'name': 'Arsenic',
    'mass': 74.9216,
    'radius_covalent': 1.21,
    'radius_VDW': 1.88,
    'color': [189, 128, 227]
}, {
    'symbol': 'Se',
    'name': 'Selenium',
    'mass': 78.971,
    'radius_covalent': 1.16,
    'radius_VDW': 1.82,
    'color': [255, 161, 0]
}, {
    'symbol': 'Br',
    'name': 'Bromine',
    'mass': 79.904,
    'radius_covalent': 1.14,
    'radius_VDW': 1.86,
    'color': [166, 41, 41]
}, {
    'symbol': 'Kr',
    'name': 'Krypton',
    'mass': 83.798,
    'radius_covalent': 1.17,
    'radius_VDW': 2.25,
    'color': [92, 184, 209]
}, {
    'symbol': 'Rb',
    'name': 'Rubidium',
    'mass': 85.4678,
    'radius_covalent': 2.1,
    'radius_VDW': 3.21,
    'color': [112, 46, 176]
}, {
    'symbol': 'Sr',
    'name': 'Strontium',
    'mass': 87.62,
    'radius_covalent': 1.85,
    'radius_VDW': 2.84,
    'color': [0, 255, 0]
}, {
    'symbol': 'Y',
    'name': 'Yttrium',
    'mass': 88.9058,
    'radius_covalent': 1.63,
    'radius_VDW': 2.75,
    'color': [148, 255, 255]
}, {
    'symbol': 'Zr',
    'name': 'Zirconium',
    'mass': 91.224,
    'radius_covalent': 1.54,
    'radius_VDW': 2.52,
    'color': [148, 224, 224]
}, {
    'symbol': 'Nb',
    'name': 'Niobium',
    'mass': 92.9064,
    'radius_covalent': 1.47,
    'radius_VDW': 2.56,
    'color': [115, 194, 201]
}, {
    'symbol': 'Mo',
    'name': 'Molybdenum',
    'mass': 95.95,
    'radius_covalent': 1.38,
    'radius_VDW': 2.45,
    'color': [84, 181, 181]
}, {
    'symbol': 'Tc',
    'name': 'Technetium',
    'mass': 97,
    'radius_covalent': 1.28,
    'radius_VDW': 2.44,
    'color': [59, 158, 158]
}, {
    'symbol': 'Ru',
    'name': 'Ruthenium',
    'mass': 101.07,
    'radius_covalent': 1.25,
    'radius_VDW': 2.46,
    'color': [36, 143, 143]
}, {
    'symbol': 'Rh',
    'name': 'Rhodium',
    'mass': 102.9055,
    'radius_covalent': 1.25,
    'radius_VDW': 2.44,
    'color': [10, 125, 140]
}, {
    'symbol': 'Pd',
    'name': 'Palladium',
    'mass': 106.42,
    'radius_covalent': 1.2,
    'radius_VDW': 2.15,
    'color': [0, 105, 133]
}, {
    'symbol': 'Ag',
    'name': 'Silver',
    'mass': 107.8682,
    'radius_covalent': 1.28,
    'radius_VDW': 2.53,
    'color': [192, 192, 192]
}, {
    'symbol': 'Cd',
    'name': 'Cadmium',
    'mass': 112.414,
    'radius_covalent': 1.36,
    'radius_VDW': 2.49,
    'color': [255, 217, 143]
}, {
    'symbol': 'In',
    'name': 'Indium',
    'mass': 114.818,
    'radius_covalent': 1.42,
    'radius_VDW': 2.43,
    'color': [166, 117, 115]
}, {
    'symbol': 'Sn',
    'name': 'Tin',
    'mass': 118.71,
    'radius_covalent': 1.4,
    'radius_VDW': 2.42,
    'color': [102, 128, 128]
}, {
    'symbol': 'Sb',
    'name': 'Antimony',
    'mass': 121.76,
    'radius_covalent': 1.4,
    'radius_VDW': 2.47,
    'color': [158, 99, 181]
}, {
    'symbol': 'Te',
    'name': 'Tellurium',
    'mass': 127.6,
    'radius_covalent': 1.36,
    'radius_VDW': 1.99,
    'color': [211, 122, 0]
}, {
    'symbol': 'I',
    'name': 'Iodine',
    'mass': 126.9045,
    'radius_covalent': 1.33,
    'radius_VDW': 2.04,
    'color': [148, 0, 148]
}, {
    'symbol': 'Xe',
    'name': 'Xenon',
    'mass': 131.293,
    'radius_covalent': 1.31,
    'radius_VDW': 2.06,
    'color': [66, 158, 176]
}, {
    'symbol': 'Cs',
    'name': 'Caesium',
    'mass': 132.9055,
    'radius_covalent': 2.32,
    'radius_VDW': 3.48,
    'color': [87, 23, 143]
}, {
    'symbol': 'Ba',
    'name': 'Barium',
    'mass': 137.327,
    'radius_covalent': 1.96,
    'radius_VDW': 3.03,
    'color': [0, 201, 0]
}, {
    'symbol': 'La',
    'name': 'Lanthanum',
    'mass': 138.9055,
    'radius_covalent': 1.8,
    'radius_VDW': 2.98,
    'color': [112, 212, 255]
}, {
    'symbol': 'Ce',
    'name': 'Cerium',
    'mass': 140.116,
    'radius_covalent': 1.63,
    'radius_VDW': 2.88,
    'color': [255, 255, 199]
}, {
    'symbol': 'Pr',
    'name': 'Praseodymium',
    'mass': 140.9077,
    'radius_covalent': 1.76,
    'radius_VDW': 2.92,
    'color': [217, 255, 199]
}, {
    'symbol': 'Nd',
    'name': 'Neodymium',
    'mass': 144.242,
    'radius_covalent': 1.74,
    'radius_VDW': 2.95,
    'color': [199, 255, 199]
}, {
    'symbol': 'Pm',
    'name': 'Promethium',
    'mass': 145,
    'radius_covalent': 1.73,
    'radius_VDW': 2.9,
    'color': [163, 255, 199]
}, {
    'symbol': 'Sm',
    'name': 'Samarium',
    'mass': 150.36,
    'radius_covalent': 1.72,
    'radius_VDW': 2.87,
    'color': [143, 255, 199]
}, {
    'symbol': 'Eu',
    'name': 'Europium',
    'mass': 151.964,
    'radius_covalent': 1.68,
    'radius_VDW': 2.83,
    'color': [97, 255, 199]
}, {
    'symbol': 'Gd',
    'name': 'Gadolinium',
    'mass': 157.25,
    'radius_covalent': 1.69,
    'radius_VDW': 2.79,
    'color': [69, 255, 199]
}, {
    'symbol': 'Tb',
    'name': 'Terbium',
    'mass': 158.9253,
    'radius_covalent': 1.68,
    'radius_VDW': 2.87,
    'color': [48, 255, 199]
}, {
    'symbol': 'Dy',
    'name': 'Dysprosium',
    'mass': 162.5,
    'radius_covalent': 1.67,
    'radius_VDW': 2.81,
    'color': [31, 255, 199]
}, {
    'symbol': 'Ho',
    'name': 'Holmium',
    'mass': 164.9303,
    'radius_covalent': 1.66,
    'radius_VDW': 2.83,
    'color': [0, 255, 156]
}, {
    'symbol': 'Er',
    'name': 'Erbium',
    'mass': 167.259,
    'radius_covalent': 1.65,
    'radius_VDW': 2.79,
    'color': [0, 230, 117]
}, {
    'symbol': 'Tm',
    'name': 'Thulium',
    'mass': 168.9342,
    'radius_covalent': 1.64,
    'radius_VDW': 2.8,
    'color': [0, 212, 82]
}, {
    'symbol': 'Yb',
    'name': 'Ytterbium',
    'mass': 173.045,
    'radius_covalent': 1.7,
    'radius_VDW': 2.74,
    'color': [0, 191, 56]
}, {
    'symbol': 'Lu',
    'name': 'Lutetium',
    'mass': 174.9668,
    'radius_covalent': 1.62,
    'radius_VDW': 2.63,
    'color': [0, 171, 36]
}, {
    'symbol': 'Hf',
    'name': 'Hafnium',
    'mass': 178.49,
    'radius_covalent': 1.52,
    'radius_VDW': 2.53,
    'color': [77, 194, 255]
}, {
    'symbol': 'Ta',
    'name': 'Tantalum',
    'mass': 180.9479,
    'radius_covalent': 1.46,
    'radius_VDW': 2.57,
    'color': [77, 166, 255]
}, {
    'symbol': 'W',
    'name': 'Tungsten',
    'mass': 183.84,
    'radius_covalent': 1.37,
    'radius_VDW': 2.49,
    'color': [33, 148, 214]
}, {
    'symbol': 'Re',
    'name': 'Rhenium',
    'mass': 186.207,
    'radius_covalent': 1.31,
    'radius_VDW': 2.48,
    'color': [38, 102, 150]
}, {
    'symbol': 'Os',
    'name': 'Osmium',
    'mass': 190.23,
    'radius_covalent': 1.29,
    'radius_VDW': 2.41,
    'color': [38, 102, 150]
}, {
    'symbol': 'Ir',
    'name': 'Iridium',
    'mass': 192.217,
    'radius_covalent': 1.22,
    'radius_VDW': 2.29,
    'color': [23, 84, 135]
}, {
    'symbol': 'Pt',
    'name': 'Platinum',
    'mass': 195.084,
    'radius_covalent': 1.23,
    'radius_VDW': 2.32,
    'color': [208, 208, 224]
}, {
    'symbol': 'Au',
    'name': 'Gold',
    'mass': 196.9666,
    'radius_covalent': 1.24,
    'radius_VDW': 2.45,
    'color': [255, 209, 35]
}, {
    'symbol': 'Hg',
    'name': 'Mercury',
    'mass': 200.592,
    'radius_covalent': 1.33,
    'radius_VDW': 2.47,
    'color': [184, 194, 208]
}, {
    'symbol': 'Tl',
    'name': 'Thallium',
    'mass': 204.38,
    'radius_covalent': 1.44,
    'radius_VDW': 2.6,
    'color': [166, 84, 77]
}, {
    'symbol': 'Pb',
    'name': 'Lead',
    'mass': 207.2,
    'radius_covalent': 1.44,
    'radius_VDW': 2.54,
    'color': [87, 89, 97]
}, {
    'symbol': 'Bi',
    'name': 'Bismuth',
    'mass': 208.9804,
    'radius_covalent': 1.51,
    'radius_VDW': 2.5,
    'color': [158, 79, 181]
}, {
    'symbol': 'Po',
    'name': 'Polonium',
    'mass': 209,
    'radius_covalent': 1.45,
    'radius_VDW': 2.5,
    'color': [171, 92, 0]
}, {
    'symbol': 'At',
    'name': 'Astatine',
    'mass': 210,
    'radius_covalent': 1.47,
    'radius_VDW': 2.5,
    'color': [117, 79, 69]
}, {
    'symbol': 'Rn',
    'name': 'Radon',
    'mass': 222,
    'radius_covalent': 1.42,
    'radius_VDW': 2.5,
    'color': [66, 130, 150]
}, {
    'symbol': 'Fr',
    'name': 'Francium',
    'mass': 223,
    'radius_covalent': 2.23,
    'radius_VDW': 2.5,
    'color': [66, 0, 102]
}, {
    'symbol': 'Ra',
    'name': 'Radium',
    'mass': 226,
    'radius_covalent': 2.01,
    'radius_VDW': 2.8,
    'color': [0, 124, 0]
}, {
    'symbol': 'Ac',
    'name': 'Actinium',
    'mass': 227,
    'radius_covalent': 1.86,
    'radius_VDW': 2.93,
    'color': [112, 170, 249]
}, {
    'symbol': 'Th',
    'name': 'Thorium',
    'mass': 232.0377,
    'radius_covalent': 1.75,
    'radius_VDW': 2.88,
    'color': [0, 186, 255]
}, {
    'symbol': 'Pa',
    'name': 'Protactinium',
    'mass': 231.0358,
    'radius_covalent': 1.69,
    'radius_VDW': 2.71,
    'color': [0, 160, 255]
}, {
    'symbol': 'U',
    'name': 'Uranium',
    'mass': 238.0289,
    'radius_covalent': 1.7,
    'radius_VDW': 2.82,
    'color': [0, 142, 255]
}, {
    'symbol': 'Np',
    'name': 'Neptunium',
    'mass': 237,
    'radius_covalent': 1.71,
    'radius_VDW': 2.81,
    'color': [0, 127, 255]
}, {
    'symbol': 'Pu',
    'name': 'Plutonium',
    'mass': 244,
    'radius_covalent': 1.72,
    'radius_VDW': 2.83,
    'color': [0, 107, 255]
}, {
    'symbol': 'Am',
    'name': 'Americium',
    'mass': 243,
    'radius_covalent': 1.66,
    'radius_VDW': 3.05,
    'color': [84, 91, 242]
}, {
    'symbol': 'Cm',
    'name': 'Curium',
    'mass': 247,
    'radius_covalent': 1.66,
    'radius_VDW': 3.38,
    'color': [119, 91, 226]
}, {
    'symbol': 'Bk',
    'name': 'Berkelium',
    'mass': 247,
    'radius_covalent': 1.68,
    'radius_VDW': 3.05,
    'color': [137, 79, 226]
}, {
    'symbol': 'Cf',
    'name': 'Californium',
    'mass': 251,
    'radius_covalent': 1.68,
    'radius_VDW': 3.0,
    'color': [160, 53, 211]
}, {
    'symbol': 'Es',
    'name': 'Einsteinium',
    'mass': 252,
    'radius_covalent': 1.65,
    'radius_VDW': 3.0,
    'color': [178, 30, 211]
}, {
    'symbol': 'Fm',
    'name': 'Fermium',
    'mass': 257,
    'radius_covalent': 1.67,
    'radius_VDW': 3.0,
    'color': [178, 30, 186]
}]


def plot(path='.',
         cubes=None,
         scale=1.0,
         font_size=16,
         font_family='Helvetica',
         width=400,
         height=400,
         show_text=True):
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

    if cubes == None:
        print(f'cube_viewer: loading cube files from the directory {path}')
        cubes = load_cubes(path)


    if len(cubes) == 0:
        print(f'cube_viewer: no cube files provided. No output will be displayed')
        return
    
    # convert cube file names into human readable text
    labels_to_filename = {}
    psi4_mo_label_re = r'Psi_([a|b])_(\d+)_(\d+)-([\w\d\'\"]*)\.cube'
    psi4_density_label_re = r'D(\w)\.cube'
    for k in cubes.keys():
        m1 = re.match(psi4_mo_label_re, k)
        m2 = re.match(psi4_density_label_re, k)
        if m1:
            label = f'MO {int(m1.groups()[1]):3d}{m1.groups()[0]} ({m1.groups()[2]}-{m1.groups()[3]})'
        elif m2:
            if m2.groups()[0] == 'a':
                label = 'Density (alpha)'
            if m2.groups()[0] == 'b':
                label = 'Density (beta)'
            if m2.groups()[0] == 's':
                label = 'Density (spin)'
            if m2.groups()[0] == 't':
                label = 'Density (total)'
        else:
            label = k
        labels_to_filename[label] = k
        
    sorted_labels = sorted(labels_to_filename.keys())

    box_layout = widgets.Layout(border='0px solid black',
                                width=f'{width + 50}px',
                                height=f'{height + 100}px')

    def f(label, cubes, labels_to_filename):
        filename = labels_to_filename[label]
        cube = cubes[filename]
        renderer = Py3JSRenderer(width=width, height=height)
        type = 'mo'
        if label[0] == 'D':
            type = 'density'
        renderer.add_cubefile(cube, scale=scale, type=type)
        style = f'font-size:{font_size}px;font-family:{font_family};font-weight: bold;'
        mo_label = widgets.HTML(
            value=f'<div align="center" style="{style}">{label}</div>')
        file_label = widgets.HTML(
            value=f'<div align="center">({filename})</div>')
        display(
            widgets.VBox([mo_label, renderer.renderer, file_label],
                         layout=box_layout))

    ws = widgets.Select(options=sorted_labels, description='Cube files:')
    interactive_widget = widgets.interactive(
        f,
        label=ws,
        cubes=widgets.fixed(cubes),
        labels_to_filename=widgets.fixed(labels_to_filename))
    output = interactive_widget.children[-1]
    output.layout.height = f'{height + 100}px'
    style = """
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
    display(widgets.HTML(style))
    display(interactive_widget)


def load_cubes(path='.'):
    """
    Load all the cubefiles (suffix ".cube" ) in a given path

    Parameters
    ----------
    path : str
        The path of the directory that will contain the cube files
    """

    import os
    cube_files = {}
    isdir = os.path.isdir(path) 
    if isdir:
        for file in os.listdir(path):
            if file.endswith('.cube'):
                cf = CubeFile()
                cf.load(os.path.join(path, file))
                cube_files[file] = cf
        if len(cube_files) == 0:
            print(f'load_cubes: no cube files found in directory {path}')
    else:
        print(f'load_cubes: directory {path} does not exist')

    return cube_files
import numpy as np
import re

class CubeFile():
    """
    A class to read, write, and manipulate cube files

    This class assumes that all coordinates (atoms, grid points)
    are stored in atomic units

    Uses code from the parse_cube function written by Andy Simmonett

    Attributes
    ----------
    data : numpy array
        The values on a grid stored as a 3d array

    Methods
    -------
    load(filename)
        Load a cube file (standard format)
    save(filename)
        Save a cube file (standard format)
    save_npz(filename)
        Save a cube file using numpy's .npz format
    load_npz(filename)
        Load a cube file using numpy's .npz format
    scale(factor)
        Multiply the data by a given factor
        Performs self.data *= factor
    add(other)
        To each grid point add the value of grid poins from another CubeFile
        Performs: self.data += other.data
    pointwise_product(other):
        Multiply every grid point with the value of grid points from another CubeFile
        Performs: self.data *= other.data
    """
    def __init__(self, filename=None):
        self.filename = filename
        self.title = None
        self.comment = None
        self.levels = []
        self.__num = [None, None, None]
        self.__min = [None, None, None]
        self.__max = [None, None, None]
        self.__inc = [None, None, None]
        self.__natoms = None
        self.__atom_numbers = None
        self.__atom_coords = None
        self.__data = None
        if self.filename:
            self.load(self.filename)

    def natoms(self):
        return self.__natoms

    def atom_numbers(self):
        return self.__atom_numbers

    def atom_coords(self):
        return self.__atom_coords

    def num(self):
        return self.__num

    def min(self):
        return self.__min

    def max(self):
        return self.__max

    def inc(self):
        return self.__inc

    def data(self):
        return self.__data

    def load(self, filename):
        with open(filename) as fp:
            self.title = fp.readline().rstrip()
            self.comment = fp.readline().rstrip()
            m = re.search(
                r"\(([-+]?[0-9]*\.?[0-9]+)\,([-+]?[0-9]*\.?[0-9]+)\)",
                self.comment)
            if (m):
                self.levels = [float(s) for s in m.groups()]

            origin = fp.readline().split()
            self.__natoms = int(origin[0])
            self.__min = tuple(float(entry) for entry in origin[1:])

            infox = fp.readline().split()
            numx = int(infox[0])
            incx = float(infox[1])

            infoy = fp.readline().split()
            numy = int(infoy[0])
            incy = float(infoy[2])

            infoz = fp.readline().split()
            numz = int(infoz[0])
            incz = float(infoz[3])

            self.__num = (numx, numy, numz)
            self.__inc = (incx, incy, incz)
            self.__max = tuple(self.__min[i] + self.__inc[i] * self.__num[i]
                             for i in range(3))

            atnums = []
            coords = []
            for atom in range(self.__natoms):
                coordinfo = fp.readline().split()
                atnums.append(int(coordinfo[0]))
                coords.append(list(map(float, coordinfo[2:])))

            self.__atom_numbers = np.array(atnums)
            self.__atom_coords = np.array(coords)

            data = np.array(
                [float(entry) for line in fp for entry in line.split()])

            if len(data) != numx * numy * numz:
                raise Exception(
                    "Number of data points is inconsistent with header in Cube file!"
                )
            self.__data = data.reshape((numx, numy, numz))

    def save(self, filename):
        with open(filename, 'w+') as fp:
            fp.write('{}\n{}\n'.format(self.title, self.comment))
            fp.write('{0:6d} {1[0]:10.6f} {1[1]:10.6f} {1[2]:10.6f}\n'.format(
                self.__natoms, self.__min))
            fp.write('{:6d} {:10.6f} {:10.6f} {:10.6f}\n'.format(
                self.__num[0], self.__inc[0], 0.0, 0.0))
            fp.write('{:6d} {:10.6f} {:10.6f} {:10.6f}\n'.format(
                self.__num[1], 0.0, self.__inc[1], 0.0))
            fp.write('{:6d} {:10.6f} {:10.6f} {:10.6f}\n'.format(
                self.__num[2], 0.0, 0.0, self.__inc[2]))
            for atom in range(self.__natoms):
                Z = self.__atom_numbers[atom]
                xyz = self.__atom_coords[atom]
                fp.write(
                    '{0:3d} {1[0]:10.6f} {1[1]:10.6f} {1[2]:10.6f}\n'.format(
                        Z, xyz))

            # flatten the data and write to disk
            flatdata = np.ndarray.flatten(self.data)
            nfullrows = len(flatdata) // 6
            fstr = '{0[0]:12.5E} {0[1]:12.5E} {0[2]:12.5E} {0[3]:12.5E} {0[4]:12.5E} {0[5]:12.5E}\n'
            for k in range(nfullrows):
                fp.write(fstr.format(flatdata[6 * k:6 * k + 6]))
            nleftover = len(flatdata) - 6 * nfullrows
            for n in range(nleftover):
                fp.write('{:12.5E} '.format(flatdata[6 * nfullrows + n]))

    def save_npz(self, filename):
        np.savez_compressed(file=filename,
                            title=self.title,
                            comment=self.comment,
                            num=self.__num,
                            __min=self.__min,
                            max=self.__max,
                            inc=self.__inc,
                            natoms=self.__natoms,
                            __atom_numbers=self.__atom_numbers,
                            __atom_coords=self.__atom_coords,
                            levels=self.levels,
                            data=self.data)

    def load_npz(self, filename):
        file = np.load(filename)
        self.title = file['title']
        self.comment = file['comment']
        self.__num = file['num']
        self.__min = file['min']
        self.__max = file['max']
        self.__inc = file['inc']
        self.__natoms = file['natoms']
        self.__atom_numbers = file['__atom_numbers']
        self.__atom_coords = file['__atom_coords']
        self.levels = file['levels']
        self.data = file['data']

    def scale(self, factor):
        # multiplication by a scalar
        if isinstance(factor, float):
            self.data *= factor

    def add(self, other):
        # add another cube file
        self.data += other.data

    def pointwise_product(self, other):
        # multiplication by a scalar
        self.data *= other.data
        self.levels = []

    def compute_levels(self,mo_type, fraction):
        sorted_data = sorted(self.__data.flatten(),key=abs,reverse=True)
        power = 2
        if mo_type == "density":
            power = 1

        neg_level = 0.0
        pos_level = 0.0
        sum = functools.reduce(lambda i, j: i + j ** power, [sorted_data[0]**power]+sorted_data[1:])
        partial_sum = 0
        for n in range(len(sorted_data)):
            partial_sum += sorted_data[n] ** power;
            if partial_sum / sum < fraction:
                if sorted_data[n] < 0.0:
                    neg_level = sorted_data[n]
                else:
                    pos_level = sorted_data[n]
            else:
                break
        return (pos_level, neg_level)

    def __str__(self):
        s = 'title: {}\ncomment: {}'.format(self.title, self.comment)
        s += '\ntotal grid points = {}'.format(self.__num[0] * self.__num[1] *
                                               self.__num[2])
        s += '\ngrid points = [{0[0]},{0[1]},{0[2]}]'.format(self.__num)
        s += '\nmin = [{0[0]:9.3f},{0[1]:9.3f},{0[2]:9.3f}]'.format(self.__min)
        s += '\nmax = [{0[0]:9.3f},{0[1]:9.3f},{0[2]:9.3f}]'.format(self.__max)
        s += '\ninc = [{0[0]:9.3f},{0[1]:9.3f},{0[2]:9.3f}]'.format(self.__inc)
        s += '\ndata = {}'.format(self.__data)
        return s

def rgb2hex(r, g, b):
    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))
    return '#%02x%02x%02x' % (r, g, b)


def xyz_to_atoms_list(xyz):
    """
    Converts an xyz geometry to a list of the form

    Parameters
    ----------
    xyz : str
        An xyz geometry where each entry has the format "<atom symbol> <x> <y> <z>".
        Any comment will be ignored

    Returns
    -------
    A list(tuple(str, float, float, float)) containing the atomic symbol and coordinates of the atom.
    """
    atoms_list = []
    re_xyz = re.compile(
        r"(\w+)\s+([-+]?[0-9]*\.?[0-9]+)\s+([-+]?[0-9]*\.?[0-9]+)\s+([-+]?[0-9]*\.?[0-9]+)"
    )
    for line in xyz.split('\n'):
        m = re.search(re_xyz, line)
        if (m):
            symbol, x, y, z = m.groups()
            atoms_list.append((symbol, float(x), float(y), float(z)))
    return atoms_list

class Py3JSRenderer():
    """
    A lightweight molecule and orbital renderer

    Attributes
    ----------
    bond_color : color
        color of the bonds
    bond_radius : float
        the radius of the bonds
    name : str
        the name of the animal
    sound : str
        the sound that the animal makes
    num_legs : int
        the number of legs the animal has (default 4)

    Methods
    -------
    display()
        Display the pythreejs renderer
    renderer()
        Return the pythreejs renderer
    add_molecule(atoms_list, bohr=False, shift_to_com=True)
        Add a molecule specified by a list of (symbol,x,y,z) tuples
    add_molecule_xyz(xyz, bohr=False, shift_to_com=True)
        Add a molecule specified in xyz format
    add_cubefile(cube,type='mo',levels=None,colors=None,colorscheme=None,opacity=1.0,scale=1.0,sumlevel=0.85,add_geom=True,shift_to_com=True)
        Add a cube file
    add_sphere(self, position, radius, color, opacity=1.0)
        Add a sphere (should not be used to draw molecules)
    add_cylinder(self, xyz1, xyz2, color, radius)
        Add a cylinder (should not be used to draw molecules)
    add_arrow(xyz1,xyz2,color,radius_small=0.1,radius_large=0.3,arrow_height=0.6)
        Add an arrow between two points
    add_plane(position,color,plane=None,normal=(0.0, 0.0, 1.0),type='circle',width=4,height=4,opacity=1.0)
        Add a plane
    def add_box(position,width,height,depth,color,opacity=1.0,normal=(0, 0, 1))
        Add a box
    """
    def __init__(self, width=400, height=400):
        """
        Class initialization function

        Parameters
        ----------
        width : int
            The width of the scene in pixels (default = 400)
        height : int
            The height of the scene in pixels (default = 400)
        """
        self.width = width
        self.height = height
        # aspect ratio
        self.aspect = float(self.width) / float(self.height)
        self.bond_radius = 0.175  # a.u.
        self.bond_color = '#555555'
        self.angtobohr = 1.88973  # TODO: use Psi4's value
        self.atom_size = 0.6  # scaling factor for atom geometry
        self.atom_geometries = {}
        self.atom_materials = {}
        self.bond_materials = {}
        self.bond_geometry = None

        # set an initial scene size
        self.camera_width = 10.0
        self.camera_height = self.camera_width / self.aspect
        self.__initialize_pythreejs_renderer()

    def display(self):
        """
        Display this renderer
        """
        display(self.renderer)

    def renderer(self):
        """
        Return the Renderer object
        """
        return self.renderer

    def show_molecule(self,wfn, shift_to_com=True):
        mol = wfn.molecule()
        natom = mol.natom()
        atoms_list = [(mol.symbol(i),mol.x(i),mol.y(i),mol.z(i)) for i in range(natom)]
        self.add_molecule(atoms_list, bohr=True)

    def add_molecule(self, atoms_list, bohr=False, shift_to_com=True):
        """
        Add a molecular geometry to the scene. The geometry is given as a list of atoms
        symbols and xyz coordinates

        Parameters
        ----------
        atoms_list : list(tuple(str, float, float, float))
            A list of tuples containing the atomic symbol and coordinates of the atom using the format
            (atomic symbol,x,y,z)
        bohr : bool
            Are the coordinate in units of bohr? (default = False)
        scale : float
            Scale factor to change the size of the scene (default = 1.0)
        shift_to_com : bool
            Shift the molecule so that the center of mass is at the origin (default = True)
        """
        if bohr == False:
            atoms_list2 = []
            for atom in atoms_list:
                symbol, x, y, z = atom
                new_atom = (symbol, self.angtobohr * x, self.angtobohr * y,
                            self.angtobohr * z)
                atoms_list2.append(new_atom)
            atoms_list = atoms_list2

        self.molecule = Group()

        # Add the atoms
        # Performance optimization using CloneArray
        # First find all the atoms of the same type
        if shift_to_com:
            Xcm, Ycm, Zcm = self.__center_of_mass(atoms_list)
        else:
            Xcm, Ycm, Zcm = (0.0, 0.0, 0.0)

        atom_positions = collections.defaultdict(list)
        for symbol, x, y, z in atoms_list:
            atom_positions[symbol].append([x - Xcm, y - Ycm, z - Zcm])
        # Then add the unique atoms at all the positions
        for atom_type in atom_positions:
            atom_mesh = self.__get_atom_mesh((atom_type, 0.0, 0.0, 0.0))
            clone_geom = CloneArray(original=atom_mesh,
                                    positions=atom_positions[atom_type])
            self.scene.add(clone_geom)

        # Add the bonds
        for i in range(len(atoms_list)):
            atom1 = atoms_list[i]
            for j in range(i + 1, len(atoms_list)):
                atom2 = atoms_list[j]
                bond = self.__get_bond_mesh(atom1, atom2)
                if bond:
                    self.scene.add(bond)
        return self.renderer

    def add_molecule_xyz(self, xyz, bohr=False, shift_to_com=True):
        """
        Add a molecular geometry in xyz format to the scene

        Parameters
        ----------
        xyz : str
            An xyz geometry where each entry has the format "<atom symbol> <x> <y> <z>".
            Any comment will be ignored
        bohr : bool
            Are the coordinate in units of bohr? (default = False)
        scale : float
            Scale factor to change the size of the scene (default = 1.0)
        shift_to_com : bool
            Shift the molecule so that the center of mass is at the origin (default = True)
        """
        atoms_list = xyz_to_atoms_list(xyz)
        self.add_molecule(atoms_list, bohr, scale)

    def add_cubefile(self,
                     cube,
                     type='mo',
                     levels=None,
                     colors=None,
                     colorscheme=None,
                     opacity=1.0,
                     scale=1.0,
                     sumlevel=0.85,
                     add_geom=True,
                     shift_to_com=True):
        """
        Add a cube file (and optionally the molecular geometry) to the scene. This function will automatically select the levels and colors
        with which to plot the surfaces

        Parameters
        ----------
        cube : CubeFile
            A CubeFile object
        type : str
            The type of cube file ('mo' or 'density')
        levels : list(float)
            The levels to plot (default = None). If not provided, levels will be automatically selected
            using the compute_levels() function of the CubeFile class. The variable sumlevel is used to
            select the levels
        color : list(str)
            The color of each surface passed as a list of hexadecimal color codes (default = None)
        colorscheme : str
            A predefined color scheme (default = 'emory'). Possible options are ['emory', 'national', 'bright', 'electron', 'wow']
        opacity : float
            Opacity of the surfaces (default = 1.0)
        scale : float
            Scale factor to change the size of the scene (default = 1.0)
        sumlevel : float
            Cumulative electron density threshold used to find the isosurface levels
        add_geom : bool
            Show the molecular geometry (default = True)
        shift_to_com : bool
            Shift the molecule so that the center of mass is at the origin (default = True)
        """
        Xcm, Ycm, Zcm = (0.0, 0.0, 0.0)
        if shift_to_com or add_geom:
            atoms_list = []
            for Z, xyz in zip(cube.atom_numbers(), cube.atom_coords()):
                symbol = ATOM_DATA[Z]['symbol']
                atoms_list.append((symbol, xyz[0], xyz[1], xyz[2]))
            # compute the center of mass
            Xcm, Ycm, Zcm = self.__center_of_mass(atoms_list)
            if add_geom:
                self.add_molecule(atoms_list,
                                  bohr=True,
                                  shift_to_com=shift_to_com)

        # compute the isosurface levels
        if not levels:
            levels = cube.compute_levels(type, sumlevel)

        # select the color scheme
        if colorscheme == 'national':
            colors = ['#e60000', '#0033a0']
        elif colorscheme == 'bright':
            colors = ['#ffcc00', '#00bfff']
        elif colorscheme == 'electron':
            colors = ['#ff00bf', '#2eb82e']
        elif colorscheme == 'wow':
            colors = ['#AC07F2', '#D7F205']
        elif colors == None or colorscheme == 'emory':
            colors = ['#f2a900', '#0033a0']

        # grab the data and extents, shift to the center of mass automatically
        data = cube.data()
        extent = [[cube.min()[0] - Xcm,
                   cube.max()[0] - Xcm],
                  [cube.min()[1] - Ycm,
                   cube.max()[1] - Ycm],
                  [cube.min()[2] - Zcm,
                   cube.max()[2] - Zcm]]
        for level, color in zip(levels, colors):
            if abs(level) > 1.0e-4:
                mesh = self.__isosurface_mesh(data,
                                              level=level,
                                              color=color,
                                              extent=extent,
                                              opacity=opacity)
                self.scene.add(mesh)

    def add_sphere(self, position, radius, color, opacity=1.0):
        """
        This function adds a sphere

        This should not be used to draw molecules because it cannot efficiently
        handle mutiple copied of the same object

        Parameters
        ----------
        position : tuple(float, float, float)
            The (x, y, z) coordinates of the center of the sphere
        radius : float
            The sphere radius
        color : str
            Hexadecimal color code
        opacity : float
            The opacity of the sphere (default = 1.0)
        """
        geometry = SphereGeometry(radius=radius,
                                  widthSegments=24,
                                  heightSegments=24)
        material = MeshStandardMaterial(color=color,
                                        roughness=0.0,
                                        metalness=0.0,
                                        side='DoubleSide',
                                        transparent=True,
                                        opacity=opacity)

        mesh = Mesh(geometry=geometry, material=material, position=position)
        self.scene.add(mesh)

    def add_cylinder(self, xyz1, xyz2, color, radius):
        """
        This function adds a cylinder/cone between two points

        This should not be used to draw molecules.

        Parameters
        ----------
        xyz1 : tuple(float, float, float)
            The (x1, y1, z1) coordinates of the beginning of the cylinder
        xyz2 : tuple(float, float, float)
            The (x2, y2, z2) coordinates of the end of the cylinder
        color : str
            Hexadecimal color code
        radius : float, (float,float), or [float,float]
            The radius of the cylinder. If a float is passed then the cylinder is
            assumed to have constant radius. If a list/tuple is passed the two numbers
            correspond to the radius at points 1 and 2. This is useful to draw cones
        """
        if isinstance(radius, float):
            mesh = self.__get_cylinder_mesh(xyz1, xyz2, radius, radius, color)
            self.scene.add(mesh)
        elif isinstance(radius, (list, tuple)):
            if len(radius) == 2:
                mesh = self.__get_cylinder_mesh(xyz1, xyz2, radius[0],
                                                radius[1], color)
                self.scene.add(mesh)
            else:
                print(
                    f'add_cylinder(): radius (= {radius}) must be either a float or a list/tuple with two elements'
                )

    def add_arrow(self,
                  xyz1,
                  xyz2,
                  color,
                  radius_small=0.1,
                  radius_large=0.3,
                  arrow_height=0.6):
        """
        This function adds an arrow  between two points

        Parameters
        ----------
        xyz1 : tuple(float, float, float)
            The (x1, y1, z1) coordinates of the beginning of the arrow
        xyz2 : tuple(float, float, float)
            The (x2, y2, z2) coordinates of the end of the arrow
        color : str
            Hexadecimal color code
        radius_small : float
            The radius of the arrow tail
        radius_large : float
            The radius of the base of the arrow cone
        arrow_height : float
            The height of the arrow cone
        """
        x1, y1, z1 = xyz1
        x2, y2, z2 = xyz2
        d = sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)
        fraction = (d - arrow_height) / d
        xyz_base = [
            x1 + (x2 - x1) * fraction, y1 + (y2 - y1) * fraction,
            z1 + (z2 - z1) * fraction
        ]
        mesh = self.__get_cylinder_mesh(xyz1, xyz_base, radius_small,
                                        radius_small, color)
        self.scene.add([mesh])
        mesh = self.__get_cylinder_mesh(xyz_base, xyz2, radius_large, 0.0,
                                        color)
        self.scene.add([mesh])

    def add_plane(self,
                  position,
                  color,
                  plane=None,
                  normal=(0.0, 0.0, 1.0),
                  type='circle',
                  width=4,
                  height=4,
                  opacity=1.0):
        """
        This function adds a plane centered at a given position. The type of plane
        can be specified either via a vector perpendicular to the plane or by selecting
        one of the planes that lies on two Cartesian axes

        Parameters
        ----------
        position : tuple(float, float, float)
            The (x, y, z) coordinates of the center of the plane
        plane : str
            The type of plane ('xy', 'xz', 'yz') (default = None). This overrides the `normal` argument
        normal : tuple(float, float, float)
            A vector (x, y, z) to which the plane is orthogonal (default = (0,0,1))
        color : str
            Hexadecimal color code
        type : str
            The type of plane ('circle', 'square') (default = 'circle')
        width : float
            The width (radius) of the plane (default = 4.0)
        height : float
            The height of the plane (default = 4.0)
        opacity : float
            The opacity of the plane (default = 1.0)
        """
        if type == 'square':
            geometry = PlaneGeometry(width=width,
                                     height=height,
                                     widthSegments=10,
                                     heightSegments=10)
        else:
            geometry = CircleGeometry(radius=width / 2, segments=48)

        material = MeshStandardMaterial(color=color,
                                        roughness=0.3,
                                        metalness=0.0,
                                        side='DoubleSide',
                                        transparent=True,
                                        opacity=opacity)

        mesh = Mesh(geometry=geometry, material=material, position=position)

        if plane == 'xy' or plane == 'yx':
            normal = (0.0, 0.0, 1.0)
        elif plane == 'xz' or plane == 'zx':
            normal = (0.0, 1.0, 0.0)
        elif plane == 'yz' or plane == 'zy':
            normal = (1.0, 0.0, 0.0)

        # If the plane is not rotated skip the rotation step
        if normal[2] != 1.0 or normal[2] != -1.0:
            R = self.__plane_rotation_matrix(normal)
            mesh.setRotationFromMatrix(R)
        self.scene.add(mesh)

    def add_box(self,
                position,
                width,
                height,
                depth,
                color,
                opacity=1.0,
                normal=(0, 0, 1)):
        """
        This function adds a box centered at a given position. The orientation of the
        box is specified via a vector perpendicular to the plane spanned by the width and height.

        Parameters
        ----------
        position : tuple(float, float, float)
            The (x, y, z) coordinates of the center of the plane
        width : float
            The width (x dimension) of the box
        height : float
            The height (y dimension) of the box
        depth : float
            The depth (z dimension) of the box
        color : str
            Hexadecimal color code
        opacity : float
            The opacity of the box (default = 1.0)
        normal : tuple(float, float, float)
            A vector (x, y, z) to which the plane is orthogonal (default = (0,0,1))
        """
        geometry = BoxGeometry(width=width,
                               height=height,
                               depth=depth,
                               widthSegments=10,
                               heightSegments=10,
                               depthSegments=10)
        material = MeshStandardMaterial(color=color,
                                        roughness=0.3,
                                        metalness=0.0,
                                        side='DoubleSide',
                                        transparent=True,
                                        opacity=opacity)

        mesh = Mesh(geometry=geometry, material=material, position=position)

        # If the bond rotation is 180 deg then return
        R = self.__plane_rotation_matrix(normal)
        mesh.setRotationFromMatrix(R)
        self.scene.add(mesh)

    def __initialize_pythreejs_renderer(self):
        """
        Create a pythreejs Scene and a Camera and add them to a Renderer
        """
        # create a Scene
        self.scene = Scene()
        # create a camera
        self.camera = OrthographicCamera(
            left=-self.camera_width / 2,
            right=self.camera_width / 2,
            top=self.camera_height / 2,
            bottom=-self.camera_height / 2,
            position=[0, 0, self.camera_height * 2.0],
            up=[0, 1, 0],
            children=[
                DirectionalLight(color='white',
                                 position=[5, 5, 1],
                                 intensity=0.5)
            ],
            near=.1,
            far=1000)

        # add the camera and some ambiend light to the scene
        self.scene.add([self.camera, AmbientLight(color='#999999')])

        self.renderer = Renderer(
            camera=self.camera,
            scene=self.scene,
            controls=[OrbitControls(controlling=self.camera)],
            width=self.width,
            height=self.height)

    def __get_atom_mesh(self, atom_info):
        """
        This function returns a Mesh object (Geometry + Material) that represents an atom

        Parameters
        ----------
        atom_info : tuple(str, float, float, float)
            A tuple containing the atomic symbol and coordinates of the atom using the format
            (atomic symbol , x, y, z)
        """
        symbol, x, y, z = atom_info
        geometry = self.__get_atom_geometry(symbol)
        material = self.__get_atom_material(symbol)
        mesh = Mesh(geometry=geometry, material=material, position=[x, y, z])
        return mesh

    def __get_atom_geometry(self, symbol, shininess=75):
        """
        This function returns a sphere geometry object with radius proportional to the covalent atomic radius

        Parameters
        ----------
        symbol : str
            The symbol of the atom (e.g. 'Li')
        shininess : int
            The shininess of the sphere (default = 75)
        """
        if symbol in self.atom_geometries:
            return self.atom_geometries[symbol]
        atom_data = ATOM_DATA[ATOM_SYMBOL_TO_Z[symbol]]
        radius_covalent = atom_data['radius_covalent'] * self.angtobohr
        geometry = SphereGeometry(radius=self.atom_size * radius_covalent,
                                  widthSegments=24,
                                  heightSegments=24)
        self.atom_geometries[symbol] = geometry
        return geometry

    def __get_atom_material(self, symbol, shininess=75):
        """
        This function returns a Material object used to draw atoms

        Parameters
        ----------
        symbol : str
            The symbol of the atom (e.g. 'Li')
        shininess : int
            The shininess of the material (default = 75)
        """
        if symbol in self.atom_materials:
            return self.atom_materials[symbol]
        atom_data = ATOM_DATA[ATOM_SYMBOL_TO_Z[symbol]]
        color = 'rgb({0[0]},{0[1]},{0[2]})'.format(atom_data['color'])
        #        material = MeshPhongMaterial(color=color, shininess=shininess)
        material = MeshStandardMaterial(color=color,
                                        roughness=0.25,
                                        metalness=0.1)
        self.atom_materials[symbol] = material
        return material

    def __get_bond_mesh(self, atom1_info, atom2_info, radius=None):
        """
        This function adds a bond between two atoms
        atoms 1 and 2

        Parameters
        ----------
        xyz1 : tuple(float, float, float)
            The (x1, y1, z1) coordinates of the beginning of the arrow
        xyz2 : tuple(float, float, float)
            The (x2, y2, z2) coordinates of the end of the arrow
        color : str
            Hexadecimal color code
        radius_small : float
            The radius of the arrow
        radius_large : float
            The radius of the arrow
        """
        symbol1, x1, y1, z1 = atom1_info
        symbol2, x2, y2, z2 = atom2_info
        d = sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)
        radius_covalent1 = ATOM_DATA[
            ATOM_SYMBOL_TO_Z[symbol1]]['radius_covalent']
        radius_covalent2 = ATOM_DATA[
            ATOM_SYMBOL_TO_Z[symbol2]]['radius_covalent']

        bond_cutoff = self.bond_cutoff(radius_covalent1, radius_covalent2)
        if d > bond_cutoff:
            return None
        if radius == None:
            radius = self.bond_radius

        d = sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)
        position = [(x2 + x1) / 2, (y2 + y1) / 2, (z2 + z1) / 2]
        geometry = self.__get_bond_geometry()
        material = self.__get_bond_material(color=self.bond_color)
        mesh = Mesh(geometry=geometry, material=material, position=position)
        mesh.scale = (1, d, 1)
        # If the bond rotation is 180 deg then return
        if y1 - y2 == d:
            mesh.rotateX(3.14159265359)  #math.pi)
            return mesh

        R = self.__cylinder_rotation_matrix([x1, y1, z1], [x2, y2, z2])
        mesh.setRotationFromMatrix(R)
        return mesh

    def __get_bond_geometry(self):
        """
        This function returns a cylinder geometry object of unit height used to draw bonds

        """
        if self.bond_geometry:
            return self.bond_geometry
        self.bond_geometry = CylinderGeometry(radiusTop=self.bond_radius,
                                              radiusBottom=self.bond_radius,
                                              height=1,
                                              radialSegments=12,
                                              heightSegments=6,
                                              openEnded=False)
        return self.bond_geometry

    def __get_bond_material(self, color, shininess=75):
        """
        This function returns a Material object used to draw bonds

        Parameters
        ----------
        color : str
            Hexadecimal color code
        shininess : int
            The shininess of the material (default = 75)
        """
        if color in self.bond_materials:
            return self.bond_materials[color]
        material = MeshStandardMaterial(color=color,
                                        roughness=0.25,
                                        metalness=0.1)
        self.bond_materials[color] = material
        return material

    def __get_cylinder_mesh(self, xyz1, xyz2, radius1, radius2, color):
        """
        This function returns a Mesh object (Geometry + Material) that represents a bond between
        atoms 1 and 2

        Parameters
        ----------
        xyz1 : tuple(float, float, float)
            The (x1, y1, z1) coordinates of atom 1
        xyz2 : tuple(float, float, float)
            The (x2, y2, z2) coordinates of atom 2
        radius1 : float
            The radius of the bond at atom 1
        radius2 : float
            The radius of the bond at atom 2
        color : str
            Hexadecimal color code
        """

        radius1 = max(0.01, radius1)
        radius2 = max(0.01, radius2)
        x1, y1, z1 = xyz1
        x2, y2, z2 = xyz2
        d = sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)
        position = [(x2 + x1) / 2, (y2 + y1) / 2, (z2 + z1) / 2]
        geometry = CylinderGeometry(radiusTop=radius2,
                                    radiusBottom=radius1,
                                    height=d,
                                    radialSegments=12,
                                    heightSegments=6,
                                    openEnded=False)
        material = MeshPhongMaterial(color=color, shininess=100)
        mesh = Mesh(geometry=geometry, material=material, position=position)

        # If the bond rotation is 180 deg then return
        if y1 - y2 == d:
            mesh.rotateX(3.14159265359)
            return mesh

        R = self.__cylinder_rotation_matrix(xyz1, xyz2)
        mesh.setRotationFromMatrix(R)
        return mesh

    def __plane_rotation_matrix(self, normal):
        """
        Computes the rotation matrix that converts a plane (circle/square) geometry in
        its standard orientation to one in which the plane is orthogonal to a given
        vector (normal). By default, planes in pythreejs are orthogonal to the vector (0,0,1),
        that is, they lay on the xy plane

        Parameters
        ----------
        normal : tuple(float, float, float)
            The vector to which we want to make a plane orthogonal
        """
        # normalize the vector
        x, y, z = normal
        d = sqrt(x**2 + y**2 + z**2)
        x /= d
        y /= d
        z /= d

        # compute the cross product: normal x (0,0,1)
        c0 = y
        c1 = -x
        c2 = 0.0

        # compute the dot product: normal . (0,0,1)
        dot = z
        c = dot
        s = sqrt(1 - c**2)

        # rotation matrix, see https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle
        R = [
            c + (1 - c) * c0**2, c0 * c1 * (1 - c), c1 * s, c0 * c1 * (1 - c),
            c + (1 - c) * c1**2, -c0 * s, -c1 * s, c0 * s, c
        ]
        return R

    def bond_cutoff(self, r1, r2):
        """
        Compute the cutoff value for displaying a bond between two atoms

        Parameters
        ----------
        r1 : float
            The radius of atom 1
        r2 : float
            The radius of atom 2
        """
        return 1.5 * self.angtobohr * (r1 + r2)

    def __cylinder_rotation_matrix(self, xyz1, xyz2):
        """
        Computes the rotation matrix that converts a cylinder geometry in its standard
        orientation to a cylinder that starts at point xyz1 and ends at xyz2

        Parameters
        ----------
        xyz1 : tuple(float, float, float)
            The (x1, y1, z1) coordinates of the beginning of the cylinder
        xyz2 : tuple(float, float, float)
            The (x2, y2, z2) coordinates of the end of the cylinder
        """
        x1, y1, z1 = xyz1
        x2, y2, z2 = xyz2
        d = sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)
        b1 = (x2 - x1) / d
        b2 = (y2 - y1) / d
        b3 = (z2 - z1) / d
        gamma = 1 / (1 + b2)
        R = [
            1 - b1 * b1 * gamma, -b1, -b1 * b3 * gamma, b1,
            1 - (b1 * b1 + b3 * b3) * gamma, b3, -b1 * b3 * gamma, -b3,
            1 - b3 * b3 * gamma
        ]
        return R

    def __isosurface_mesh(self, data, level, color, extent=None, opacity=1.0):
        """
        This function returns a Mesh object (Geometry + Material) for an isosurface

        Parameters
        ----------
        data : numpy.ndarray
            A 3D array containing the values on a grid
        level : float
            The isosurface level. This must be included in the range of values on the grid
        color : str
            Hexadecimal code for the color used to display the surface
        extent : list
            list of [[xmin, xmax], [ymin, ymax], [zmin, zmax]] values that define the bounding box of the mesh,
            otherwise the viewport is used
        opacity : float
            The opacity of the surface (default = 1.0)
        """
        vertices, faces = self.__compute_isosurface(data,
                                                    level=level,
                                                    color=color,
                                                    extent=extent)

        # Create the geometry
        isoSurfaceGeometry = Geometry(vertices=vertices, faces=faces)

        # Calculate normals per vertex for round edges
        isoSurfaceGeometry.exec_three_obj_method('computeVertexNormals')

        if opacity == 1.0:
            material = MeshStandardMaterial(vertexColors='VertexColors',
                                            roughness=0.3,
                                            metalness=0.0,
                                            side='DoubleSide',
                                            transparent=False)
        else:
            material = MeshStandardMaterial(vertexColors='VertexColors',
                                            roughness=0.3,
                                            metalness=0.0,
                                            side='DoubleSide',
                                            transparent=True,
                                            opacity=opacity)

        # Create a mesh
        isoSurfaceMesh = Mesh(geometry=isoSurfaceGeometry, material=material)

        return isoSurfaceMesh

    def __compute_isosurface(self, data, level, color, extent=None):
        """
        Compute the vertices and faces of an isosurface from grid data

        Parameters
        ----------
        data : numpy.ndarray
            Grid data stored as a numpy 3D tensor
        level : float
            The isocontour value that defines the surface
        color :
            color of a face
        extent : list
            list of [[xmin, xmax], [ymin, ymax], [zmin, zmax]] values that define the bounding box of the mesh,
            otherwise the viewport is used

        Returns
        -------
        a tuple of vertices and faces
        """
        values = skimage.measure.marching_cubes_lewiner(data, level)
        sk_verts, sk_faces, normals, values = values
        x, y, z = sk_verts.T

        # Rescale coordinates to given limits
        if extent:
            xlim, ylim, zlim = extent
            x = x * np.diff(xlim) / (data.shape[0] - 1) + xlim[0]
            y = y * np.diff(ylim) / (data.shape[1] - 1) + ylim[0]
            z = z * np.diff(zlim) / (data.shape[2] - 1) + zlim[0]

        # Assemble the list of vertices
        vertices = []
        for n in range(len(x)):
            vertices.append([x[n], y[n], z[n]])

        # Assemble the list of faces
        faces = []
        for face in sk_faces:
            i, j, k = face
            faces.append((i, j, k, None, (color, color, color), None))
        return (vertices, faces)

    def __molecule_extents(self, atoms_list):
        """
        Compute the extent of a molecule

        Parameters
        ----------
        atoms_list : list(tuple(str, float, float, float))
            A list of tuples containing the atomic symbol and coordinates of the atom using the format
            (atomic symbol,x,y,z)

        Returns
        -------
        A tuple(float, float, float, float, float, float)  containing the minimum and maximum
        coordinates of this molecule in the format (minx, maxx, miny, maxy, minz, maxz)
        """
        minx = min(map(lambda x: x[1], atoms_list))
        maxx = min(map(lambda x: x[1], atoms_list))
        miny = min(map(lambda x: x[2], atoms_list))
        maxy = min(map(lambda x: x[2], atoms_list))
        minz = min(map(lambda x: x[3], atoms_list))
        maxz = min(map(lambda x: x[3], atoms_list))
        return (minx, maxx, miny, maxy, minz, maxz)

    def __center_of_mass(self, atoms_list):
        """
        This function returns the center of mass of a molecule

        Parameters
        ----------
        atoms_list : list(tuple(str, float, float, float))
            A list of tuples containing the atomic symbol and coordinates of the atom using the format
            (atomic symbol,x,y,z)
        """
        X = 0.0
        Y = 0.0
        Z = 0.0
        M = 0.0
        for (symbol, x, y, z) in atoms_list:
            mass = ATOM_DATA[ATOM_SYMBOL_TO_Z[symbol]]['mass']
            X += mass * x
            Y += mass * y
            Z += mass * z
            M += mass
        return (X / M, Y / M, Z / M)

