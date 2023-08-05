# -*- coding: utf-8 -*-
import sys
""" Topoly Parameters
This module contains common parameters for various functions used in Topoly
"""

class Closure:
    """
    Type of closure.
    """
    CLOSED = 0
    """ (deterministic) direct segment between two endpoints """
    MASS_CENTER = 1
    """ (deterministic) segments added to two endpoints in the direction "going out of center of mass", and then connected by an arc on the big sphere"""
    TWO_POINTS = 2
    """ (random) each endpoint connected with different random point on the big sphere, and those added points connected by an arc on the big sphere"""
    ONE_POINT = 3
    """ (random) both endpoints connected with the same random point on the big sphere"""
    RAYS = 4
    """ (random) parallel segments added to two endpoints, and then connected by an arc on the big sphere; direction of added segments is random"""
    DIRECTION = 5
    """ (deterministic) the same as RAYS but the direction can be given"""


class ReduceMethod:
    """
    Reduction Method
    """
    KMT = 1
    """ KMT algorithm [ Koniaris K, Muthukumar M (1991) Self-entanglement in ring polymers, J. Chem. Phys. 95, 2873–2881 ]. This algorithm analyzes all triangles in a chain made by three consecutive amino acids, and removes the middle amino acid in case a given triangle is not intersected by any other segment of the chain. In effect, after a number of iterations, the initial chain is replaced by (much) shorter chain of the same topological type."""
    REIDEMEISTER = 2
    """ Simplification of chain (and number of crossings) by a sequence of Reidemeister moves."""
    EASY = 3
    """ The deterministic version of Reidemeister simplification, using only the 1st and 2nd move."""


class GlnMode:
    """
    Modes for GLN calculations in function gln()
    """
    BASIC = 0
    """ GLN value between two whole chains is calculated. """
    MAX = 1
    """ Additionally some info about the maximal |GLN| value between fragments of two chains is calculated.
        The dictionary with the maximal |GLN| value between chain1 and pieces of chain2 (with indices)
        and vice versa is returned.
        In the dictionary there is also GLN value between whole chains and local maximum.
        Local maximum is calculated when another argument of function gln() -- density_for_max (d) -- 
        is larger than 0 (by default is -1) and maximal |GLN| value between all pairs of fragments of two chains
        that have lengths being a multiplication of d is calculated. Thus for d=1 all pairs of fragments 
        are analyzed. For longer chains d=1 is highly unrecommended due to high time and space complexity 
        of computations ( O(N^4/d^4) ).
        
        Further arguments of function gln() used in this mode: density_for_max. 
        """
    AVG = 2
    """ Additionally the average GLN value after number of random closures of both chains is calculated. 
        
        Further arguments of function gln() used in this mode: avg_tries. 
        """
    MATRIX = 3
    """ Whole GLN matrix between chain1 and all subchains of chain2 is calculated. 
        As a result the matrix (M) of the size of chain2_length x chain2_length is returned, and
        M[i][j] is GLN value between chain1 and fragment of chain2 from i-th to j-th atom.
        
        Further arguments of function gln() used in this mode: matrix_plot_format, matrix_plot_fname, 
                                                               matrix_output_format, matrix_output_fname. 
        """

class SurfacePlotFormat:
    DONTPLOT = 0
    VMD = 1
    JSMOL = 2
    MATHEMATICA = 4


class TopolyException(Exception):
    pass


class PlotFormat:
    PNG = 'png'
    SVG = 'svg'
    PDF = 'pdf'


class OutputFormat:
    """
    The output formats for the matrices.
    """
    KnotProt = 'knotprot'
    """ The matrix in the format used in KnotProt"""
    Dictionary = 'dict'
    """ The dictionary-like output"""
    Matrix = 'matrix'
    """ The matrix-like (list of lists) output"""
    Ccode = 'Ccode'
    """ The output suitable for passing to C-coded parts of the package"""


class PrecisionSurface:
    """
    Precision of computations of minimal surface spanned on the loop (high precision => time consuming computations).
    """
    HIGH = 0
    """ The highest precision, default for single structure. """
    MEDIUM = 1
    """ Two lower precision levels, may be used when analyzing large structures, trajectories or other big sets of data."""
    LOW = 2


class DensitySurface:
    """
    Density of the triangulation of minimal surface spanned on the loop (high precision => time consuming computations).
    Default value: MEDIUM.
    """
    HIGH = 2
    MEDIUM = 1
    LOW = 0

class Bridges:
    """
    The bridges types to be parsed from PDB file.
    """
    SSBOND = 'ssbond'
    ION = 'ion'
    COVALENT = 'covalent'
    ALL = 'all'


class OutputType:
    """
    The possible output types for find_loops, find_thetas, etc.
    """
    PDcode = 'pdcode'
    EMcode = 'emcode'
    XYZ = 'xyz'
    NXYZ = 'nxyz'
    PDB = 'pdb'
    Mathematica = 'math'
    MMCIF = 'mmcif'
    PSF = 'psf'
    IDENT = 'ident'
    TOPOLOGY = 'topology'
    ATOMS = 'atoms'
    


class OutputTypeLasso:
    """
    The possible output types for lasso_type.
    """
    MainType = 0
    """ Only lasso type as a string, i.e. L1. """
    MoreInfo = 1
    """ Lasso type and other information in a dictionary, i.e. 
        
        {"cl": "L1", "beforeN": [], "beforeC": ["-15","+43","-44"], "crossingsN": [],
        "crossingsC": ["-15"], "surface_area": 14.524, "loop_length": 31.821,
        "Rg": 2.735, "smoothing_iterations": 0},
        
        where 
        - "crossingsN/C" are ids of atoms that cross the surface, 
        - "beforeN/C" are ids of atoms that cross the surface before the procedure
        of reduction of shallow (and possibly misleading) crossings;
        - "smoothing_iterations" is the number of iterations of structure smoothing procedure
        that has been performed not changing lasso type (if parameter <smooth> was used
        in lasso_type() function);
        - "Rg" is radius of giration of whole chain (possibly smoothed)
    """

class Colors:
    """
    Colors for drawing figures.
    """
    Knots = {'name': 'knot', '51': 'Reds', '61': 'Blues', '31': 'Greens', '52': 'Purples', '41': 'Oranges'}
    GLN = {'name': 'GLN', '': 'seismic'}
    Structure = {'name': 'structure', 'all': 'hsv'}
    Writhe = {'name': 'writhe', 'all': 'Spectral'}
    # def colorFromGLN(gln):
    #     if (gln < -1):
    #         return (int(255 * 1 / (gln * gln)), 0, 0)
    #     elif (gln <= 0):
    #         return (255, int(255 * (1 + gln)), int(255 * (1 + gln)))
    #     elif (gln <= 1):
    #         return (int(255 * (1 - gln)), int(255 * (1 - gln)), 255)
    #     else:
    #         return (0, 0, int(255 * 1 / (gln * gln)))

def test(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except:
            print('  Error occurred:', sys.exc_info()[0], sys.exc_info()[1])
            return None
    return wrapper
