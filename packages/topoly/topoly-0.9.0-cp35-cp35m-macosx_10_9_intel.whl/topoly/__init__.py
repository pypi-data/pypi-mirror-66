#!/usr/bin/python3
"""
The main Topoly module collecting the functions designed for the users.

Pawel Dabrowski-Tumanski
p.dabrowski at cent.uw.edu.pl
04.09.2019

Documentation generated with Sphinx: www.sphinx-doc.org

Support in PyCharm:
https://www.jetbrains.com/help/pycharm/settings-tools-python-integrated-tools.html
- change default reStructuredText to Google

Docs will be published in: https://readthedocs.org/
"""

from .manipulation import *
from .invariants import *
from topoly.topoly_knot import *
from topoly.topoly_preprocess import *
from .codes import *
from .plotting import KnotMap, Reader
from .params import *
from .polygongen import *
from .lasso import Lasso
from .convert import convert_xyz2vmd
from .knotcon import create, export


def alexander(input_data, closure=Closure.TWO_POINTS, tries=200, boundaries=None,
              reduce_method=ReduceMethod.KMT, max_cross=15, poly_reduce=True, translate=True,
              external_dictionary='', hide_trivial=True, chiral=False, matrix=False, density=1,
              level=0, matrix_plot=False, plot_ofile="KnotFingerPrintMap", matrix_cutoff=0.48,
              plot_format=PlotFormat.PNG, output_file='', output_format=OutputFormat.Dictionary,
              cuda=True, run_parallel=True, parallel_workers=None, palette=Colors.Knots,
              arrows=True, chain=None, bridges_type=None, model=None, debug=False):
    """
    Calculates the Alexander polynomial of the given structure.

    Args:
        input_data (str/list):
                The structure to calculate the polynomial
                for, given in abstract code, coordinates, or the path to
                the file containing the data.
        closure (str, optional):
                The method to close the chain. Viable options are the
                parameters of the topoly.params.Closure.
                Default: Closure.TWO_POINTS.
        tries (int, optional):
                The number of tries for stochastic closure methods.
                Default: 200.
        boundaries (list of [int, int], optional):
                The boundaries of the subchains to be checked. The
                subchains are specified as a list of subchain beginning
                and ending index. If empty, the whole chain is
                calculated. Default: None.
        reduce_method (str, optional):
                The method of chain reduction. Viable options are the
                parameters of the ReduceMethod class.
                Default: ReduceMethod.KMT.
        max_cross (int, optional):
                The maximal number of crossings after reduction to start
                the polynomial calculation. Default: 15.
        poly_reduce (bool, optional):
                If the polynomial should be presented in the reduced
                form. Default: False.
        translate (bool, optional):
                If translate the polynomial to the structure topology
                using the dictionary. Default: False.
        external_dictionary (str, optional):
                The path to the file with the external dictionary of the
                polynomials. Default: ''.
        hide_trivial (bool, optional):
                If to suppress printing out the trivial results.
                Default: True
        chiral (bool, optional):
                If the chirality should be taken into account.
                By default False.
        matrix (bool, optional):
                if to calculate the whole matrix i.e. the polynomial for
                each subchain. Default: False.
        density (int, optional):
                the inverse of resolution of matrix calculation. Higher
                number speeds up calculation, but may result in omitting
                some non-trivial subchains. Default: 1.
        level (float, optional):
                The cutoff of the non-trivial structure probability. If
                0, all the subchains with at least one non-trivial
                closure are treated as non-trivial. Default: 0.
        matrix_plot (bool, optional):
                If to plot a figure of a matrix (knot fingerprint).
                Default: False.
        plot_ofile (str, optional):
                The name of the matrix figure plot.
                Default: KnotFingerPrintMap.
        plot_format (str, optional):
                The format of the matrix figure plot. Viable formats are
                the parameters of the PlotFormat class.
                Default: PlotFormat.PNG.
        output_file (str, optional):
                The name of the file with the matrix results. If empty,
                the resulting matrix is returned to source. Default: ''.
        output_format (str, optional):
                The format of the matrix output. The viable formats are
                the parameters of the OutputFormat class.
                Default: OutputFormat.DICTIONARY.
        cuda (bool, optional):
                If to use the cuda-provided acceleration if possible.
                Default: True.
        run_parallel (bool, optional):
                If to use the Python-provided parallelization of
                calculation. Default: True.
        parallel_workers (int, optional):
                Number of parallel workers. If 0, all the available
                processors will be used. Default: 0.
        debug (bool, optional):
                The debug mode. Default: False.

    Returns:
        The dictionary with the Alexander polynomial results. For each
        subchain a separate dictionary with different polynomial
        probabilities is created.
    """
    result = Invariant(input_data, chain=chain, model=model, bridges_type=bridges_type)
    return result.calculate(
                AlexanderGraph, closure=closure, tries=tries, boundaries=boundaries,
                reduce_method=reduce_method, max_cross=max_cross, poly_reduce=poly_reduce,
                translate=translate, external_dictionary=external_dictionary,
                hide_trivial=hide_trivial, chiral=chiral, matrix=matrix, density=density,
                level=level, matrix_plot=matrix_plot, plot_ofile=plot_ofile,
                matrix_cutoff=matrix_cutoff, plot_format=plot_format, output_file=output_file,
                output_format=output_format, cuda=cuda, run_parallel=run_parallel,
                parallel_workers=parallel_workers, palette=palette, arrows=arrows, debug=debug)


def jones(input_data, closure=Closure.TWO_POINTS, tries=200, boundaries=None,
          reduce_method=ReduceMethod.KMT, max_cross=15, poly_reduce=True, translate=True,
          external_dictionary='', hide_trivial=True, chiral=False, matrix=False, density=1,
          level=0, matrix_plot=False, plot_ofile="KnotFingerPrintMap", matrix_cutoff=0.48,
          plot_format=PlotFormat.PNG, output_file='', output_format=OutputFormat.Dictionary,
          cuda=True, run_parallel=True, parallel_workers=None, palette=Colors.Knots, arrows=True,
          chain=None, bridges_type=None, model=None, debug=False):
    """
    Calculates the Jones polynomial of the given structure.

    Parameters are the same as in topoly.alexander_.

    Returns:
        The dictionary with the Jones polynomial results. For each
        subchain a separate dictionary with different polynomial
        probabilities is created.
    """
    result = Invariant(input_data, chain=chain, model=model, bridges_type=bridges_type)
    return result.calculate(
                JonesGraph, closure=closure, tries=tries, boundaries=boundaries,
                reduce_method=reduce_method, max_cross=max_cross, poly_reduce=poly_reduce,
                translate=translate, external_dictionary=external_dictionary,
                hide_trivial=hide_trivial, chiral=chiral, matrix=matrix, density=density,
                level=level, matrix_plot=matrix_plot, plot_ofile=plot_ofile,
                matrix_cutoff=matrix_cutoff, plot_format=plot_format, output_file=output_file,
                output_format=output_format, cuda=cuda, run_parallel=run_parallel,
                parallel_workers=parallel_workers, palette=palette, arrows=arrows, debug=debug)


def conway(input_data, closure=Closure.TWO_POINTS, tries=200, boundaries=None,
           reduce_method=ReduceMethod.KMT, max_cross=15, poly_reduce=True, translate=True,
           external_dictionary='', hide_trivial=True, chiral=False, matrix=False, density=1,
           level=0, matrix_plot=False, plot_ofile="KnotFingerPrintMap", matrix_cutoff=0.48,
           plot_format=PlotFormat.PNG, output_file='', output_format=OutputFormat.Dictionary,
           cuda=True, run_parallel=True, parallel_workers=None, palette=Colors.Knots, arrows=True,
           chain=None, bridges_type=None, model=None, debug=False):
    """
    Calculates the Conway polynomial of the given structure.

    Parameters are the same as in topoly.alexander_.

    Returns:
        The dictionary with the Conway polynomial results. For each
        subchain a separate dictionary with different polynomial
        probabilities is created.
    """
    result = Invariant(input_data, chain=chain, model=model, bridges_type=bridges_type)
    return result.calculate(
                ConwayGraph, closure=closure, tries=tries, boundaries=boundaries,
                reduce_method=reduce_method, max_cross=max_cross, poly_reduce=poly_reduce,
                translate=translate, external_dictionary=external_dictionary,
                hide_trivial=hide_trivial, chiral=chiral, matrix=matrix, density=density,
                level=level, matrix_plot=matrix_plot, plot_ofile=plot_ofile,
                matrix_cutoff=matrix_cutoff, plot_format=plot_format, output_file=output_file,
                output_format=output_format, cuda=cuda, run_parallel=run_parallel,
                parallel_workers=parallel_workers, palette=palette, arrows=arrows, debug=debug)


def homfly(input_data, closure=Closure.TWO_POINTS, tries=200, boundaries=None,
           reduce_method=ReduceMethod.KMT, max_cross=15, poly_reduce=True, translate=True,
           external_dictionary='', hide_trivial=True, chiral=False, matrix=False, density=1,
           level=0, matrix_plot=False, plot_ofile="KnotFingerPrintMap", matrix_cutoff=0.48,
           plot_format=PlotFormat.PNG, output_file='', output_format=OutputFormat.Dictionary,
           cuda=True, run_parallel=True, parallel_workers=None, palette=Colors.Knots, arrows=True,
           chain=None, bridges_type=None, model=None, debug=False):
    """
    Calculates the HOMFLY-PT polynomial of the given structure.

    Parameters are the same as in topoly.alexander_.

    Returns:
        The dictionary with the HOMFLY-PT polynomial results. For each
        subchain a separate dictionary with different polynomial
        probabilities is created.
    """
    result = Invariant(input_data, chain=chain, model=model, bridges_type=bridges_type)
    return result.calculate(
                HomflyGraph, closure=closure, tries=tries, boundaries=boundaries,
                reduce_method=reduce_method, max_cross=max_cross, poly_reduce=poly_reduce,
                translate=translate, external_dictionary=external_dictionary,
                hide_trivial=hide_trivial, chiral=chiral, matrix=matrix, density=density,
                level=level, matrix_plot=matrix_plot, plot_ofile=plot_ofile,
                matrix_cutoff=matrix_cutoff, plot_format=plot_format, output_file=output_file,
                output_format=output_format, cuda=cuda, run_parallel=run_parallel,
                parallel_workers=parallel_workers, palette=palette, arrows=arrows, debug=debug)


def yamada(input_data, closure=Closure.TWO_POINTS, tries=200, boundaries=None,
           reduce_method=ReduceMethod.KMT, max_cross=15, poly_reduce=True, translate=True,
           external_dictionary='', hide_trivial=True, chiral=False, matrix=False, density=1,
           level=0, matrix_plot=False, plot_ofile="KnotFingerPrintMap", matrix_cutoff=0.48,
           plot_format=PlotFormat.PNG, output_file='', output_format=OutputFormat.Dictionary,
           cuda=True, run_parallel=True, parallel_workers=None, palette=Colors.Knots, arrows=True,
           chain=None, bridges_type=None, model=None, debug=False):
    """
    Calculates the Yamada polynomial of the given structure.

    Parameters are the same as in topoly.alexander_.

    Returns:
        The dictionary with the Yamada polynomial results. For each
        subchain a separate dictionary with different polynomial
        probabilities is created.
    """
    result = Invariant(input_data, chain=chain, model=model, bridges_type=bridges_type)
    return result.calculate(
                YamadaGraph, closure=closure, tries=tries, boundaries=boundaries,
                reduce_method=reduce_method, max_cross=max_cross, poly_reduce=poly_reduce,
                translate=translate, external_dictionary=external_dictionary,
                hide_trivial=hide_trivial, chiral=chiral, matrix=matrix, density=density,
                level=level, matrix_plot=matrix_plot, plot_ofile=plot_ofile,
                matrix_cutoff=matrix_cutoff, plot_format=plot_format, output_file=output_file,
                output_format=output_format, cuda=cuda, run_parallel=run_parallel,
                parallel_workers=parallel_workers, palette=palette, arrows=arrows, debug=debug)


def kauffman_bracket(input_data, closure=Closure.TWO_POINTS, tries=200, boundaries=None,
                reduce_method=ReduceMethod.KMT, max_cross=15, poly_reduce=True, translate=True,
                external_dictionary='', hide_trivial=True, chiral=False, matrix=False, density=1,
                level=0, matrix_plot=False, plot_ofile="KnotFingerPrintMap", matrix_cutoff=0.48,
                plot_format=PlotFormat.PNG, output_file='', output_format=OutputFormat.Dictionary,
                cuda=True, run_parallel=True, parallel_workers=None, palette=Colors.Knots,
                arrows=True, chain=None, bridges_type=None, model=None, debug=False):
    """
    Calculates the Kauffman bracket of the given structure.

    Parameters are the same as in topoly.alexander_.

    Returns:
        The dictionary with the Kauffman bracket results. For each
        subchain a separate dictionary with different polynomial
        probabilities is created.
    """
    result = Invariant(input_data, chain=chain, model=model, bridges_type=bridges_type)
    return result.calculate(
                KauffmanBracketGraph, closure=closure, tries=tries, boundaries=boundaries,
                reduce_method=reduce_method, max_cross=max_cross, poly_reduce=poly_reduce,
                translate=translate, external_dictionary=external_dictionary,
                hide_trivial=hide_trivial, chiral=chiral, matrix=matrix, density=density,
                level=level, matrix_plot=matrix_plot, plot_ofile=plot_ofile,
                matrix_cutoff=matrix_cutoff, plot_format=plot_format, output_file=output_file,
                output_format=output_format, cuda=cuda, run_parallel=run_parallel,
                parallel_workers=parallel_workers, palette=palette, arrows=arrows, debug=debug)


def kauffman_polynomial(input_data, closure=Closure.TWO_POINTS, tries=200, boundaries=None,
                reduce_method=ReduceMethod.KMT, max_cross=15, poly_reduce=True, translate=True,
                external_dictionary='', hide_trivial=True, chiral=False, matrix=False, density=1,
                level=0, matrix_plot=False, plot_ofile="KnotFingerPrintMap", matrix_cutoff=0.48,
                plot_format=PlotFormat.PNG, output_file='', output_format=OutputFormat.Dictionary,
                cuda=True, run_parallel=True, parallel_workers=None, palette=Colors.Knots,
                arrows=True, chain=None, bridges_type=None, model=None, debug=False):
    """
    Calculates the Kauffman two-variable polynomial of the given structure.

    Parameters are the same as in topoly.alexander_.

    Returns:
        The dictionary with the Kauffman two-variable polynomial
        results. For each subchain a separate dictionary with different
        polynomial probabilities is created.
    """
    result = Invariant(input_data, chain=chain, model=model, bridges_type=bridges_type)
    return result.calculate(
                KauffmanPolynomialGraph, closure=closure, tries=tries, boundaries=boundaries,
                reduce_method=reduce_method, max_cross=max_cross, poly_reduce=poly_reduce,
                translate=translate, external_dictionary=external_dictionary,
                hide_trivial=hide_trivial, chiral=chiral, matrix=matrix, density=density,
                level=level, matrix_plot=matrix_plot, plot_ofile=plot_ofile,
                matrix_cutoff=matrix_cutoff, plot_format=plot_format, output_file=output_file,
                output_format=output_format, cuda=cuda, run_parallel=run_parallel,
                parallel_workers=parallel_workers, palette=palette, arrows=arrows, debug=debug)


def blmho(input_data, closure=Closure.TWO_POINTS, tries=200, boundaries=None,
          reduce_method=ReduceMethod.KMT, max_cross=15, poly_reduce=True, translate=True,
          external_dictionary='', hide_trivial=True, chiral=False, matrix=False, density=1,
          level=0, matrix_plot=False, plot_ofile="KnotFingerPrintMap", matrix_cutoff=0.48,
          plot_format=PlotFormat.PNG, output_file='', output_format=OutputFormat.Dictionary,
          cuda=True, run_parallel=True, parallel_workers=None, palette=Colors.Knots, arrows=True,
          chain=None, bridges_type=None, model=None, debug=False):
    """
    Calculates the BLM/Ho polynomial of the given structure.

    Parameters are the same as in topoly.alexander_.

    Returns:
        The dictionary with the BLM/Ho polynomial results. For each
        subchain a separate dictionary with different polynomial
        probabilities is created.
    """
    result = Invariant(input_data, chain=chain, model=model, bridges_type=bridges_type)
    return result.calculate(
                BlmhoGraph, closure=closure, tries=tries, boundaries=boundaries,
                reduce_method=reduce_method, max_cross=max_cross, poly_reduce=poly_reduce,
                translate=translate, external_dictionary=external_dictionary,
                hide_trivial=hide_trivial, chiral=chiral, matrix=matrix, density=density,
                level=level, matrix_plot=matrix_plot, plot_ofile=plot_ofile,
                matrix_cutoff=matrix_cutoff, plot_format=plot_format, output_file=output_file,
                output_format=output_format, cuda=cuda, run_parallel=run_parallel,
                parallel_workers=parallel_workers, palette=palette, arrows=arrows, debug=debug)


def aps(input_data, closure=Closure.TWO_POINTS, tries=200, boundaries=None,
        reduce_method=ReduceMethod.KMT, max_cross=15, poly_reduce=True, translate=True,
        external_dictionary='', hide_trivial=True, chiral=False, matrix=False, density=1,
        level=0, matrix_plot=False, plot_ofile="KnotFingerPrintMap", matrix_cutoff=0.48,
        plot_format=PlotFormat.PNG, output_file='', output_format=OutputFormat.Dictionary,
        cuda=True, run_parallel=True, parallel_workers=None, palette=Colors.Knots, arrows=True,
        chain=None, bridges_type=None, model=None, debug=False):
    """
    Calculates the APS bracket of the given structure.

    Parameters are the same as in topoly.alexander_.

    Returns:
        The dictionary with the APS bracket results. For each subchain
        a separate dictionary with different polynomial probabilities is
        created.
    """
    result = Invariant(input_data, chain=chain, model=model, bridges_type=bridges_type)
    return result.calculate(
                ApsGraph, closure=closure, tries=tries, boundaries=boundaries,
                reduce_method=reduce_method, max_cross=max_cross, poly_reduce=poly_reduce,
                translate=translate, external_dictionary=external_dictionary,
                hide_trivial=hide_trivial, chiral=chiral, matrix=matrix, density=density,
                level=level, matrix_plot=matrix_plot, plot_ofile=plot_ofile,
                matrix_cutoff=matrix_cutoff, plot_format=plot_format, output_file=output_file,
                output_format=output_format, cuda=cuda, run_parallel=run_parallel,
                parallel_workers=parallel_workers, palette=palette, arrows=arrows, debug=debug)


def writhe(input_data, closure=Closure.TWO_POINTS, tries=200, boundaries=None,
              reduce_method=ReduceMethod.KMT, max_cross=15, poly_reduce=True, translate=True,
              external_dictionary='', hide_trivial=True, chiral=False, matrix=False, density=1,
              level=0, matrix_plot=False, plot_ofile="KnotFingerPrintMap", matrix_cutoff=0.48,
              plot_format=PlotFormat.PNG, output_file='', output_format=OutputFormat.Dictionary,
              cuda=True, run_parallel=True, parallel_workers=None, palette=Colors.Knots,
              arrows=True, chain=None, bridges_type=None, model=None, debug=False):
    """"
    Calculates writhe of a given structure.

    Parameters are the same as in topoly.alexander_.

    Returns:
        The dictionary with the writhe results. For each subchain
        a separate dictionary with different polynomial probabilities
        is created.
    """
    result = Invariant(input_data, chain=chain, model=model, bridges_type=bridges_type)
    return result.calculate(
                WritheGraph, closure=closure, tries=tries, boundaries=boundaries,
                reduce_method=reduce_method, max_cross=max_cross, poly_reduce=poly_reduce,
                translate=translate, external_dictionary=external_dictionary,
                hide_trivial=hide_trivial, chiral=chiral, matrix=matrix, density=density,
                level=level, matrix_plot=matrix_plot, plot_ofile=plot_ofile,
                matrix_cutoff=matrix_cutoff, plot_format=plot_format, output_file=output_file,
                output_format=output_format, cuda=cuda, run_parallel=run_parallel,
                parallel_workers=parallel_workers, palette=palette, arrows=arrows, debug=debug)


#TODO: Proponuje zmienic wszedzie nazwy argumentow chain, chain1 etc. na chain_id, chain1_id..
#      Zeby nie mylilo sie to z tym, ze piszemy (co najmniej ja;) w opisie, ze np. badamy GLN pomiedzy chain1 i chain2 - wtedy chain1 to jest
#      caly moj lancuch, cala krzywa, a nie jego nazwa.
def gln(input_data, chain2_data=None, chain1_boundary=(-1, -1),
        chain2_boundary=(-1, -1), mode = GlnMode.BASIC,
        max_density=-1, avg_tries=200, matrix_plot=False, matrix_plot_format=PlotFormat.PNG,
        matrix_plot_fname="GLN_map", matrix_output_format=OutputFormat.Matrix,
        matrix_output_fname='', precision_output=3, chain1_id=None, model1=None, chain2_id=None,
        model2=None, debug=False):
    """
    Calculates gaussian linking number between two chains.

    Args:
        input_data (str/list):
                the structure containing two chains that may be linked
                -- or one chain and second one is given in another
                argument, chain2_data -- given in coordinates, or the
                path to the file containing the data.
        chain2_data (str/list, optional):
                the structure containing the second chain, given in
                coordinates, or the path to the file containing the
                data. If not given, both chains are expected to be
                present in the input_data. Default: None
        chain1_boundary ([int, int], optional):
                the indices of chain1 within the input_data. If [-1, -1]
                the whole structure is used as chain1.
                Default: [-1, -1]
        chain2_boundary ([int, int], optional):
                the indices delimiting chain2. If [-1, -1], the whole
                structure is treated as chain2. Note, that if the
                chain2_data is not specified separately, boundaries must
                be given for both chains (as both of them are taken then
                from input_data and they cannot overlap).
                Default: [-1, -1]
        mode (int, optional):
                mode of calculations, viable formats are parameters
                of the GlnMode class. The basic option (GlnMode.BASIC)
                calculates one value -- gaussian linking number between
                two whole chains. Other modes give a possibility of
                calculating maximal |GLN| value between fragments of two
                chains (GlnMode.MAX), average GLN value after number of
                random closures of both chains (GlnMode.AVE) or whole
                GLN matrix between chain1 and all subchains of chain2
                (GlnMode.MATRIX). For each mode there are further
                arguments that may be specified.
                Default: GlnMode.BASIC
        max_density (int, optional):
                in mode GlnMode.MAX: if max_density (d)=1,
                all pairs of fragments are analyzed; if d>1 then
                only fragments of length being a multiplication of d are
                analyzed. For longer chains d=1 is highly unrecommended
                due to high time and space complexity of computations
                (O(N^4/d^4)). If -1, local maximum is not calculated.
                Default: -1
        avg_tries (int, optional):
                in mode GlnMode.AVG: the number of closures performed
                in calculating the average GLN value. Defaulf: 200
        matrix_plot_format (str, optional):
                in mode GlnMode.MATRIX: the format of the plot with the
                matrix of GLN -- if the plot should be prepared. Viable
                formats are parameters of the PlotFormat class.
                Default: PlotFormat.DONTPLOT
        matrix_plot_fname (str, optional):
                in mode GlnMode.MATRIX: the name of the file containing
                the matrix plot. Default: 'GLN_map'
        matrix_output_format (str, optional):
                in mode GlnMode.MATRIX: the format of the matrix output
                data. Viable formats are the parameters of the
                OutputFormat class. Default: OutputFormat.Matrix
        matrix_output_fname (str, optional):
                in mode GlnMode.MATRIX: if not empty, it indicates the
                name of the file to save the matrix calculation results.
                Default: ''
        precision_output (int, optional):
                precision of output, number of decimal places in
                returned values. Default: 3
        chain1_id (str, optional):
                Name of chain one wants to choose from PDB file
                (important if "input_data" is a PDB file, where might be
                lots of different chains) to construct chain1. If None,
                first chain in PDB file is choosen. Default: None
        model1 (str, optional):
                Name of model one wants to choose from PDB file
                (important if "input_data" is a PDB file, where might be
                lots of different models) to construct chain1. If None,
                first model in PDB file is choosen. Default: None
        chain2_id (str, optional):
                Name of chain one wants to choose from PDB file
                (important if "input_data"/"chain2_data" is a PDB file,
                where might be lots of different chains) to construct
                chain2. If None, first chain in PDB file is choosen.
                Default: None
        model2 (str, optional):
                Name of model one wants to choose from PDB file
                (important if "input_data"/"chain2_data" is a PDB file,
                where might be lots of different models) to construct
                chain2. If None, first model in PDB file is choosen.
                Default: None
        debug (bool, optional):
                the debug mode. Default: False

    Returns:
        The value of the Gaussian Linking Number calculated between two
        chains (which may be called loop and tail), specified either in
        separate files, or by the indices (tail_boundary). In maximal
        GLN mode (GlnMode.MAX), the dictionary with the maximal |GLN|
        between two chains, as well as maximal |GLN| between one chain
        and the part of the second chain (indicated by the indices) is
        returned. In matrix mode (GlnMode.MATRIX), the whole matrix of
        GLN between one chain (the loop) and each subchain of second
        chain (tail) is calculated.
    """
    result = GlnGraph(input_data)
    return result.calculate(
                chain2=chain2_data, boundary=chain1_boundary, boundary2=chain2_boundary,
                mode=mode, max_density=max_density, avg_tries=avg_tries, matrix_plot=matrix_plot, 
                matrix_plot_format=matrix_plot_format, plot_ofile=matrix_plot_fname, 
                output_file=matrix_output_fname, output_format=matrix_output_format, 
                precision=precision_output, debug=debug)


def getpoly(invariant, topolname, value=None):
    """
    Generates list of objects which have polynomial value corresponding
    to given invariant type and topolname. These objects can be
    multiplied (*) to find polynomial of joined structures and added (+)
    to find polynomial of unjoined union.

    Args:
        invariant (str):
                Name of invariant (or its abbreviation):
                'Alexander' ('a'), 'Conway' ('c'), 'Jones' ('j'),
                'HOMFLYPT' ('h'), 'Yamada' ('y'), 'BLMHo' ('b'),
                'Kauffman bracket' ('kb'), 'Kauffman polynomial' ('kp'),
        topolname (str):
                Topology name i.e. "3_1", "-5_1", "t3_1"
        value(str, optional):
                Polynomial of given topolname structure. If nothing is
                given searches for linkname value in polvalues.py.
                Default: None.

    Returns:
        List of Polynomial objects.
    """
    return create(invariant, topolname, value)


def exportpoly(polynomials, exportfile='new_polvalues.py'):
    """
    Sends list of Polynomial objects generated by getpoly to chosen
    exportfile, that can be used as an alternative dictionary.

    Args:
        polynomials (list of Poly objects):
                List of objects generated by getpoly.
        exportfile (str, optional):
                Name of file where polynomial reocrds will be written.
                Default: 'new_polvalues.py'.

    """
    return export(polynomials, exportfile)


def make_surface(input_data, loop_indices=None, precision=PrecisionSurface.HIGH,
            density=DensitySurface.MEDIUM, precision_output=3, chain=None, model=None,
            bridges_type=Bridges.SSBOND):
    """
    Calculates minimal surface spanned on a given loop.

    Args:
        input_data (str/list):
                The structure containing loop to calculate the surface
                spanned on, given in coordinates, or the path to the
                file containing the data.
        loop_indices (list, optional):
                The indices of loop within the input_data. If they are
                not specified the whole structure is used as loop.
                Default: None.
        precision (int, optional):
                Precision of computations of minimal surface. Viable
                options are the parameters of the PrecisionSurface
                class. Default: PrecisionSurface.HIGH.
        density (int, optional):
                Density of the triangulation of minimal surface. Viable
                options are the parameters of the DensitySurface class.
                Default: DensitySurface.MEDIUM.
        precision_output (int, optional):
                Precision of output, number of decimal places in
                returned values. Default: 3
        chain (str, optional):
                Name of chain one wants to analyze (important if
                "input_data" is a PDB file, where might be lots of
                different chains). Default: None
        model (str, optional):
                Name of model one wants to analyze (important if
                "input_data" is a PDB file, where might be lots of
                different models). Default: None
        bridges_type (str, optional):
                The bridges types to be parsed from PDB file and define
                loops (if they are not specified by loop_indices
                argument). Viable options are the parameters of the
                Bridges class. Default: Bridges.SSBOND

    Returns:
        List of triangles that form minimal surface.
    """
    obj = Lasso(input_data, loop_indices)
    return obj.make_surface(precision, density, precision_output)


def lasso_type(input_data, loop_indices=None, smooth=0, precision=PrecisionSurface.HIGH,
               density=DensitySurface.MEDIUM, min_dist=(10, 3, 3),
               pic_files=SurfacePlotFormat.DONTPLOT, output_prefix='',
               output_type=OutputTypeLasso.MainType, chain=None, model=None,
               bridges_type=Bridges.SSBOND):
    """
    Calculates minimal surfaces spanned on given loops and checks if
    remaining parts of chains cross surfaces and how many times.
    Returns corresponding topoly types of lassos (type for each loop).

    Args:
        input_data: (str/list):
                The structure containing the loop which may be pierced
                by the tail, given in coordinates, or the path to the
                file containing the data.
        loop_indices (list, optional):
                the indices of all loops within the input_data (list of
                pairs). If they are not specified, SS-bonds defining
                loops are authomatically found in input data (if the
                file is in PDB or CIF format). Default: None
                #TODO: TO NA RAZIE NIE DZIALA (to do PAWLA/BARTKA)
        smooth (int, optional):
                Number of smoothing iterations. Higher number
                -- structure will be more smooth. Default: 0.
        precision (int, optional):
                Precision of computations of minimal surface. Viable
                options are the parameters of the PrecisionSurface
                class. Default: PrecisionSurface.HIGH.
        density (int, optional):
                Density of the triangulation of minimal surface. Viable
                options are the parameters of the DensitySurface class.
                Default: DensitySurface.MEDIUM
        min_dist ([int, int, int], optional):
                Minimal distance (number of atoms/aminoacids etc.)
                between, respectively, next two crossings, crossing and
                bridge defining loop and crossing and end of tail -- to
                think about these crossings as deep enough ones and do
                NOT reduce them. Default: [10,3,3]
        pic_files (int/list of ints, optional):
                Format of output files for generated pictures with
                surface and crossings. Possible formats (VMD, JSmol,
                Mathematica) are the parameters of the SurfacePlotFormat
                class. For instance pic_files may equal
                SurfacePlotFormat.DONTPLOT
                or [SurfacePlotFormat.VMD, SurfacePlotFormat.JSMOL].
                Default: SurfacePlotFormat.DONTPLOT
        output_prefix (str, optional):
                Prefix of desired output file. Default: No prefix.
        output_type (int, optional):
                Report format, viable options are the parameters
                of the OutputTypeLasso class (just lasso type in string
                or much information in dictionary).
                Default: OutputTypeLasso.MainType
        chain (str, optional):
                Name of chain one wants to analyze (important if
                "input_data" is a PDB file, where might be lots of
                different chains). Default: None
        model (str, optional):
                Name of model one wants to analyze (important if
                "input_data" is a PDB file, where might be lots of
                different models). Default: None
        bridges_type (str, optional):
                The bridges types to be parsed from PDB file and define
                loops (if they are not specified by loop_indices
                argument). Viable options are the parameters of the
                Bridges class. Default: Bridges.SSBOND

    Returns:
        Dictionary with loops indices as keys and string reports (just
        lasso type) or dictionary reports (dictonary with more
        information like ids of all crossings, more info in
        OutputTypeLasso class in params.py) as values.

    """
    obj = Lasso(input_data, loop_indices)
    return obj.lasso_type(
                smooth, precision, density, min_dist, pic_files, output_prefix, output_type)


def find_loops(structure, output_type=OutputType.PDcode, chain=None, bridges_type=Bridges.SSBOND,
               model=None, arc_bridges=0, output='list', file_prefix='loop', folder_prefix=''):
    """
    Finds all loops in a given structure and return as one of many
    possible formats.

    Args:
        structure (str/list):
                The structure to calculate the polynomial for, given in
                abstract code, coordinates, or the path to the file
                containing the data.
        output_type (str, optional):
                The output format of the loops. The viable formats are
                parameters of the OutputType class.
                Default: OutputType.TOPOLOGY.
        chain (str, optional): the chain identifier in the PDB file.
        model (int, optional): the model identifier in the PDB file.
        arc_bridges (int, optional): number of bridges which can
                compose a given loop. Default: 1.
        output (str, optional):
                Format of output data 'file', 'list' or 'generator'.
        file_prefix (str, optional):
                Only if output=='file'. Prefix of each created file.
                Default: "loop".
        folder_prefix (str, optional):
                Only if output=='file'. Prefix of created file folder.
                Default: no prefix.

    Returns:
        List of found loops represented in a chosen format.
    """
    g = Graph(structure, chain=chain, model=model, bridges_type=bridges_type)
    return g.find_loops(output_type=output_type, arc_bridges=arc_bridges, output=output, file_prefix=file_prefix,
                        folder_prefix=folder_prefix)


def find_links(structure, output_type=OutputType.PDcode, chain=None, bridges_type=Bridges.SSBOND,
               model=None, arc_bridges=1, output='list', file_prefix='loop', folder_prefix='', components=2):
    """
    Finds all loops in a given structure and return as one of many
    possible formats.

    Args:
        structure (str/list):
                The structure to calculate the polynomial for, given in
                abstract code, coordinates, or the path to the file
                containing the data.
        output_type (str, optional):
                The output format of the loops. The viable formats are
                parameters of the OutputType class.
                Default: OutputType.TOPOLOGY.

    Returns:
        List of found loops represented in a chosen format.
    """
    g = Graph(structure, chain=chain, model=model, bridges_type=bridges_type)
    return g.find_links(output_type=output_type, arc_bridges=arc_bridges, output=output, file_prefix=file_prefix,
                        folder_prefix=folder_prefix, components=components)


def find_thetas(structure, output_type=OutputType.PDcode, chain=None, bridges_type=Bridges.SSBOND,
               model=None, arc_bridges=1, output='list', file_prefix='loop', folder_prefix=''):
    """
    Finds all theta-curves in a given structure and return as one of
    many possible formats.

    Args:
        structure (str/list):
                The structure to calculate the polynomial for, given in
                abstract code, coordinates, or the path to the file
                containing the data.
        output_type (str, optional):
                The output format of the loops. The viable formats are
                parameters of the OutputType class.
                Default: OutputType.TOPOLOGY.

    Returns:
        List of found theta-curves represented in a chosen format.
    """
    g = Graph(structure, chain=chain, model=model, bridges_type=bridges_type)
    return g.find_thetas(output_type=output_type, arc_bridges=arc_bridges, output=output, file_prefix=file_prefix,
                        folder_prefix=folder_prefix)


def find_handcuffs(structure, output_type=OutputType.PDcode, chain=None, bridges_type=Bridges.SSBOND,
               model=None, arc_bridges=1, output='list', file_prefix='loop', folder_prefix=''):
    """
    Finds all handcuffs in a given structure and return as one of many
    possible formats.

    Args:
        structure (str/list):
                The structure to calculate the polynomial for, given in
                abstract code, coordinates, or the path to the file
                containing the data.
        output_type (str, optional):
                The output format of the loops. The viable formats are
                parameters of the OutputType class.
                Default: OutputType.TOPOLOGY.

    Returns:
        List of found handcuffs represented in a chosen format.
    """
    g = Graph(structure, chain=chain, model=model, bridges_type=bridges_type)
    return g.find_handcuffs(output_type=output_type, arc_bridges=arc_bridges, output=output, file_prefix=file_prefix,
                        folder_prefix=folder_prefix)


# TODO - test it! - Wanda!
def generate_walk(length, no_of_structures, bond_length=1, print_with_index=True, output='file',
                file_prefix='walk', folder_prefix='', file_fmt=(3, 5)):
    """
    Generates polygonal lasso structure with vertices of equal lengths
    and saves in .xyz file. Each structures is saved in distinct file
    named <file_prefix>_<num>.xyz in folder l<looplength>_t<taillength>.

    Args:
        length (int):
                Number of sides of polygonal random walk.
        no_of_structures (int):
                Quantity of created walks.
        bond_length (int, optional):
                Length of each side of created walks. Default: 1.
        print_with_index (bool, optional):
                If True, then output has also node index. Default: True.
        output (str, optional):
                Format of output data 'file', 'list' or 'generator'.
        file_prefix (str, optional):
                Only if output=='file'. Prefix of each created file.
                Default: "walk".
        folder_prefix (str, optional):
                Only if output=='file'. Prefix of created file folder.
                Default: no prefix.
        file_fmt ([int,int], optional):
                Only if output=='file'. Numbers on file and folder
                format <num>, <length> are padded with maximally these
                numbers of zeros respectively.

    Returns:
        If output == 'file': comunicate with folder name
        If output == 'list': list structures, each structure is
                             coordinate list of lists
        If output == 'generator': generator yealding structure which is
                                  coordinate list of lists
    """
    if output == 'file':
        P = Polygon_walk(length, no_of_structures, bond_length, print_with_index, file_prefix,
                         folder_prefix, file_fmt)
        return P.export_polyg_xyz()
    elif output == 'list':
        P = Polygon_walk(length, no_of_structures, bond_length, print_with_index, file_prefix,
                         folder_prefix, file_fmt)
        return P.export_polyg_list()
    elif output == 'generator':
        return generate_polygon('walk', n=no_of_structures, walk_length=length, no_of_structures=1,
                                bond_length=bond_length, print_with_index=print_with_index,
                                file_prefix=file_prefix, folder_prefix=folder_prefix,
                                file_fmt=file_fmt)
    else: raise NameError('Parameter \'output\' accepts only \'file\', \'list\' and \'generator\''\
                           'arguments')


def generate_loop(length, no_of_structures, bond_length=1, print_with_index=True, output='file',
                file_prefix='loop', folder_prefix='', file_fmt=(3, 5)):
    """
    Generates polygonal loop structure with vertices of equal lengths
    and saves in .xyz file. Each structures is saved in distinct file
    named <file_prefix>_<num>.xyz in folder w<length>.

    Args:
        length (int):
                Number of sides of polygonal loops.
        no_of_structures (int):
                Quantity of created loops.
        bond_length (int, optional):
                Length of each side of created loops. Default: 1.
        print_with_index (bool, optional):
                If True, then created .xyz has nxyz format instead of
                xyz, where n is index number. Default: True.
        output (str, optional):
                Format of output data 'file', 'list' or 'generator'.
        file_prefix (str, optional):
                Only if output=='file'. Prefix of each created file.
                Default: "loop".
        folder_prefix (str, optional):
                Only if output=='file'. Prefix of created file folder.
                Default: no prefix.
        file_fmt ([int,int], optional):
                Only if output=='file'. Numbers on file and folder
                format <num>, <looplength> are padded with maximally
                these numbers of zeros respectively.

    Returns:
        If output == 'file': comunicate with folder name
        If output == 'list': list structures, each structure is
                             coordinate list of lists
        If output == 'generator': generator yealding structure which is
                                  coordinate list of lists
    """
    if output == 'file':
        P = Polygon_loop(length, no_of_structures, bond_length, print_with_index, file_prefix,
                         folder_prefix, file_fmt)
        return P.export_polyg_xyz()
    elif output == 'list':
        P = Polygon_loop(length, no_of_structures, bond_length, print_with_index, file_prefix,
                         folder_prefix, file_fmt)
        return P.export_polyg_list()
    elif output == 'generator':
        return generate_polygon('loop', n=no_of_structures, loop_length=length, no_of_structures=1,
                                bond_length=bond_length, print_with_index=print_with_index,
                                file_prefix=file_prefix, folder_prefix=folder_prefix,
                                file_fmt=file_fmt)
    else: raise NameError('Parameter \'output\' accepts only \'file\', \'list\' and \'generator\''\
                           'arguments')


def generate_lasso(looplength, taillength, no_of_structures, bond_length=1, output='file',
                print_with_index=True, file_prefix='lasso', folder_prefix='', file_fmt=(3, 3, 5)):
    """
    Generates polygonal lasso structure with vertices of equal lengths
    and saves in .xyz file. Each structures is saved in distinct file
    named <file_prefix>_<num>.xyz in folder l<looplength>_t<taillength>.

    Args:
        looplength (int):
                Number of sides of polygonal loop.
        taillength (int):
                Number of sides of polygonal tail.
        no_of_structures (int):
                Quantity of created loops.
        bond_length (int, optional):
                Length of each side of created lassos. Default: 1.
        print_with_index (bool, optional):
                If True, then created .xyz has nxyz format instead of
                xyz, where n is index number. Default: True.
        output (str, optional):
                Format of output data 'file', 'list' or 'generator'.
        file_prefix (str, optional):
                Only if output=='file'. Prefix of each created file.
                Default: "lasso".
        folder_prefix (str, optional):
                Only if output=='file'. Prefix of created file folder.
                Default: no prefix.
        file_fmt ([int,int,int], optional):
                Only if output=='file'. Numbers on file and folder
                format <num>, <looplength>, <taillength> are padded with
                maximally these numbers of zeros respectively.

    Returns:
        If output == 'file': comunicate with folder name
        If output == 'list': list structures, each structure is
                             coordinate list of lists
        If output == 'generator': generator yealding structure which is
                                  coordinate list of lists
    """
    if output == 'file':
        P = Polygon_lasso(looplength, taillength, no_of_structures, bond_length, print_with_index,
                          file_prefix, folder_prefix, file_fmt)
        return P.export_polyg_xyz()
    elif output == 'list':
        P = Polygon_lasso(looplength, taillength, no_of_structures, bond_length, print_with_index,
                          file_prefix, folder_prefix, file_fmt)
        return P.export_polyg_list()
    elif output == 'generator':
        return generate_polygon('lasso', n=no_of_structures, loop_length=looplength,
                                tail_length=taillength, no_of_structures=1, bond_length=bond_length,
                                print_with_index=print_with_index, file_prefix=file_prefix,
                                folder_prefix=folder_prefix, file_fmt=file_fmt)
    else: raise NameError('Parameter \'output\' accepts only \'file\', \'list\' and \'generator\''\
                           'arguments')


def generate_handcuff(looplengths, linkerlength, no_of_structures, bond_length=1, output='file',
                print_with_index=True, file_prefix='hdcf', folder_prefix='', file_fmt=(3, 3, 3, 5)):
    """
    Generates polygonal lasso structure with vertices of equal lengths
    and saves in .xyz file. Each structures is saved in distinct file
    named <file_prefix>_<num>.xyz in folder
    l<looplength1>_<looplength2>_t<linkerlength>.

    Args:
        looplengths ([int,int]):
                Number of sides of polygonal loops.
        linkerlength (int):
                Number of sides of polygonal linker.
        no_of_structures (int):
                Quantity of created loops.
        bond_length (int, optional):
                Length of each side of created lassos. Default: 1.
        print_with_index (bool, optional):
                If True, then created .xyz has nxyz format instead of
                xyz, where n is index number. Default: True.
        output (str, optional):
                Format of output data 'file', 'list' or 'generator'.
        file_prefix (str, optional):
                Only if output=='file'. Prefix of each created file.
                Default: "hdcf".
        folder_prefix (str, optional):
                Only if output=='file'. Prefix of created file folder.
                Default: no prefix.
        file_fmt ([int,int,int,int], optional):
                Only if output=='file'. Numbers on file and folder
                format <num>, <looplength1>, <looplength2>,
                <linkerlength> are padded with maximally these numbers
                of zeros respectively.

    Returns:
        If output == 'file': comunicate with folder name
        If output == 'list': list structures, each structure is
                             coordinate list of lists
        If output == 'generator': generator yealding structure which is
                                  coordinate list of lists
    """
    if output == 'file':
        P = Polygon_handcuff(looplengths, linkerlength, no_of_structures, bond_length,
                             print_with_index, file_prefix, folder_prefix, file_fmt)
        return P.export_polyg_xyz()
    elif output == 'list':
        P = Polygon_handcuff(looplengths, linkerlength, no_of_structures, bond_length,
                             print_with_index, file_prefix, folder_prefix, file_fmt)
        return P.export_polyg_list()
    elif output == 'generator':
        return generate_polygon('handcuff', n=no_of_structures, loop_lengths = looplengths,
                                linker_length = linkerlength, no_of_structures=1,
                                bond_length=bond_length, print_with_index=print_with_index,
                                file_prefix=file_prefix, folder_prefix=folder_prefix,
                                file_fmt=file_fmt)
    else: raise NameError('Parameter \'output\' accepts only \'file\', \'list\' and \'generator\''\
                           'arguments')


def generate_link(looplengths, loop_dist, no_of_structures, bond_length=1, output='file',
                print_with_index=True, file_prefix='link', folder_prefix='', file_fmt=(3, 3, 3, 5)):
    """
    Generates polygonal lasso structure with vertices of equal lengths
    and saves in .xyz file. Each structures is saved in distinct file
    named <file_prefix>_<num>.xyz in folder
    l<looplength1>_<looplength2>_d<loop_dist>.

    Args:
        looplengths ([int,int]):
                Number of sides of polygonal loops.
        loop_dist (float):
                Distance between geometrical centers of loops measured
                in multiples of bond_length.
        no_of_structures (int):
                Quantity of created loops.
        bond_length (int, optional):
                Length of each side of created lassos. Default: 1.
        print_with_index (bool, optional):
                If True, then created .xyz has nxyz format instead of
                xyz, where n is index number. Default: True.
        output (str, optional):
                Format of output data 'file', 'list' or 'generator'.
        file_prefix (str, optional):
                Only if output=='file'. Prefix of each created file.
                Default: "link".
        file_fmt ([int,int,int,int], optional):
                Only if output=='file'. Numbers on file and folder
                format <num>, <looplength1>, <looplength2>, <loop_dist>
                are padded with maximally these numbers of zeros
                respectively.

    Returns:
        If output == 'file': comunicate with folder name
        If output == 'list': list structures, each structure is
                             coordinate list of lists
        If output == 'generator': generator yealding structure which is
                                  coordinate list of lists
    """
    if output == 'file':
        P = Polygon_link(looplengths, loop_dist, no_of_structures, bond_length, print_with_index,
                         file_prefix, folder_prefix, file_fmt)
        return P.export_polyg_xyz()
    elif output == 'list':
        P = Polygon_link(looplengths, loop_dist, no_of_structures, bond_length, print_with_index,
                         file_prefix, folder_prefix, file_fmt)
        return P.export_polyg_list()
    elif output == 'generator':
        return generate_polygon('link', n=no_of_structures, loop_lengths=looplengths,
                                loop_dist = loop_dist, no_of_structures=1,
                                bond_length=bond_length, print_with_index=print_with_index,
                                file_prefix=file_prefix, folder_prefix=folder_prefix,
                                file_fmt=file_fmt)
    else: raise NameError('Parameter \'output\' accepts only \'file\', \'list\' and \'generator\''\
                           'arguments')


def plot_matrix(matrix, plot_ofile="KnotFingerPrintMap", plot_format=PlotFormat.PNG, cutoff=0.48,
                palette=Colors.Knots, arrows=True, debug=False):
    """
    Plotting the figure for a given fingerprint matrix.

    Args:
        matrix (str):
                The matrix with information about the topology of each
                subchain of the structure. Can be given either in
                dictionary, or KnotProt format. The matrix can be given
                directly, or as a path to the file.
        plot_ofile (str, optional):
                The name of the output file with the matrix figure.
                Default: KnotFingerPrintMap.
        plot_format (str, optional):
                The format of the output matrix figure. Viable options
                are the parameters of the PlotFormat class.
                Default: PlotFormat.PNG.
        cutoff (float, optional):
                The cutoff of the non-trivial structure probability. All
                structures with probability below the cutoff will be
                regarded as trivial, and therefore not marked in the
                figure. Default: 0.48.
        palette (str, optional):
                The palette of colors for matrix plot. Viable options
                are parameters of the Palette class.
                Default: Palette.KNOT.
        arrows (bool, optional):
                If the arrows are to be plotted. Default: True
        debug (bool, optional):
                The debug mode.

    Returns:
        Communicate about the figure creation.
    """
    return manipulation.plot_matrix(
                matrix, plot_ofile=plot_ofile, plot_format=plot_format, palette=palette,
                arrows=arrows, cutoff=cutoff, debug=debug)


def find_spots(matrix, gap_size=0, spot_size=20, cutoff=0.48):
    """
    Finds centers of fields in the matrix.

    Args:
        matrix (str/dict):
                The matrix fingerprint of the structure.
        gap_size (int, optional):
                The size of the trivial fragment allowed between two
                parts to classify them as single spot. If 0, only the
                connected fragments are considered as spots. Default: 0.
        spot_size (int, optional):
                The minimal size of the spot. Fragments with less
                non-trivial repentants will be suppressed. Default: 20.
    Returns:
        The list of the centers of the spots.
    """
    return find_spots_centers(matrix, gap_size=gap_size, spot_size=spot_size)


def translate_matrix(matrix, output_format=OutputFormat.Dictionary, knot='', beg=0, end=0):
    """
    Changes format of given matrix (??).

    Args:
        matrix(??):
        output_format(??):
        knot(??):
        beg(??):
        end(??):

    Returns:
        ???

    """
    if type(matrix) is str and os.path.isfile(matrix):
        with open(matrix, 'r') as myfile:
            data = myfile.read()
    else:
        data = matrix
    if output_format == OutputFormat.Dictionary:
        return data2dictionary(data, knot=knot, beg=beg)
    elif output_format == OutputFormat.KnotProt:
        return data2knotprot(data, beg=beg, end=end, knot=knot)
    elif output_format == OutputFormat.Matrix:
        return data2matrix(data)
    else:
        raise TopolyException("Unknown output format.")


def xyz2vmd(xyz_file):
    """
    Converts .xyz file into .pdb file and creates .psf topoly file with
    same name. Then you can open your structure in vmd typing
    "vmd file.pdb -psf file.psf".

    .xyz file format:
        4 columns (id, x, y, z), atoms in neighboring rows are
        treated as bonded, lines with single letter (e.g. X) separate
        different arcs.

    Args:
        xyz_file (str):
                Name of xyz file.
    Returns:
        None
    """
    return convert_xyz2vmd(xyz_file)


def plot_graph(structure, palette=Colors.Structure):
    """
    Plotting the 3D rotable presentation of the structure with each arc
    colored differently.

    Args:
        structure (str/list):
                The structure to calculate the polynomial for, given in
                abstract code, coordinates, or the path to the file
                containing the data.
        palette (str, optional):
                The palette of colors for matrix plot. Viable options
                are parameters of the Palette class.
                Default: Palette.RAINBOW.

    Returns:
        Communicate about the figure creation.
    """
    g = Graph(structure)
    g.plot(palette)
    return


def translate_code(structure, output_type=OutputType.PDcode):
    """
    Translates between the abstract codes.

    Args:
        structure (str/list):
                The structure to calculate the polynomial for, given in
                abstract code, coordinates, or the path to the file
                containing the data.
        output_type (str, optional):
                The output format of the loops. The viable formats are
                parameters of the OutputType class.
                Default: OutputType.PDcode.

    Returns:
        The structure in a given format.
    """
    g = Graph(structure)
    return g.print_data(output_type=output_type)


def find_matching(data, invariant, chiral=False, external_dictionary=''):
    """
    Finds the matching structure for a given polynomial. Searches either
    the built-in, or user-defined dictionary.

    Args:
        data (string/dictionary):
                The polynomial given either in string of coefficients
                (e.g. '1 -1 1'),
                the dictionary of polynomials with their probabilities
                (e.g. {'1 -1 1': 0.8, '1 -3 1': 0.2},
                or dictionary of probabilities for each subchain (e.g.
                {(0, 100): {'1 -1 1': 0.8, '1 -3 1': 0.2},
                (50, 100): {'1 -1 1': 0.3, '1': 0.7}}).
        invariant (string):
                The name of the invariant, e.g. 'Alexander', of 'Jones'.
        chiral (bool, optional):
                If the chirality should be taken into account.
                By default False.
        external_dictionary (string, optional):
                The absolute path to the user-defined dictionary of
                polynomials. The dictionary must be compliant with the
                template which can be obtained on the Topoly website
                (https://topoly.cent.uw.edu.pl).

    Returns:
        Either the string with matching structure name (e.g. '3_1'), or
        the dictionary with the structure name and respective
        probability (e.g. {'3_1': 0.8, '4_1': 0.2}), or the dictionary
        with data for each subchain, e.g.
        {(0, 100): {'3_1': 0.8, '4_1': 0.2},
        (50, 100): {'3_1': 0.3, '0_1': 0.7}}.
    """
    return find_matching_structure(
                data, invariant, chiral=chiral, external_dictionary=external_dictionary)


def import_structure(structure_name):
    """
    Finds a PDcode of the structure required and creates a corresponding
    graph.

    Args:
        structure_name (str):
                The name of the structure to create.

    Returns:
        The graph of the corresponding structure defined by the PDcode.
    """
    code = ''
    structure_name = structure_name.strip()
    if structure_name in PD.keys():
        code = PD[structure_name]
    else:
        for key in PD.keys():
            if re.sub('\.[1-9]*', '', re.sub('[-+*]', '', key)) == structure_name:
                code = PD[key]
                break
    if not code:
        raise TopolyException('The structure ' + str(structure_name) + ' is not available in the local library.')
    return code



def reduce_structure(structure, reduce_method=ReduceMethod.KMT, output_type=OutputType.XYZ, steps=1000,
           debug=False):
    """
    Reducing the structure to a form with less crossing in a planar
    projection.

    Args:
        structure (str/list):
                The structure to calculate the polynomial for, given in
                abstract code, coordinates, or the path to the file
                containing the data.
        reduce_method (str):
                The method used to reduce the structure. Viable methods
                are the parameters of the ReduceMethod class.
                Default: ReduceMethod.KMT.
        output_type (str):
                The format of the reduced chain. The abstract codes are
                possible only for closed structure.
                Default: OutputType.XYZ.

    Returns:
        The abstract code or the coordinates of the reduced structure.
    """
    g = Graph(structure)
    if not g.closed:
        raise TopolyException("The curve is not closed. Use topoly.close_curve first.")
    abstract_reduction = [ReduceMethod.EASY, ReduceMethod.REIDEMEISTER]
    abstract_output = [OutputType.EMcode, OutputType.PDcode]
    if reduce_method in abstract_reduction and output_type not in abstract_output:
        raise TopolyException("With chosen reduction method only the abstract codes are possible")
    g.reduce(method=reduce_method, steps=steps, debug=debug)
    return g.print_data(output_type=output_type)


def close_curve(structure, closure=Closure.TWO_POINTS, output_type=OutputType.XYZ, debug=False):
    """
    Closing the structure (connecting loose ends) with a chosen method.

    Args:
        structure (str/list):
                The structure to calculate the polynomial for, given in
                abstract code, coordinates, or the path to the file
                containing the data.
        closure (str):
                The method used to close the structure. Viable methods
                are the parameters of the Closure class.
                Default: Closure.TWO_POINTS.
        output_type (str):
                The format of the reduced chain.
                Default: OutputType.XYZ.

    Returns:
        The abstract code or the coordinates of the closed structure.
    """
    g = Graph(structure)
    g.close(method=closure, debug=debug)
    return g.print_data(output_type=output_type)

