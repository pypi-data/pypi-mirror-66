# Topoly

Protein knots and lassos search tools from the INTERDISCIPLINARY LABORATORY of BIOLOGICAL SYSTEMS MODELLING, University of Warsaw, Warsaw, Poland

This package provides a set of executable programs as well as a shared library with a Python 3 wrapper.  

1. knotnet
2. homflylink
3. surfacesmytraj
4. ncuclinks
5. lmpoly
6. gln

## Requirements
1. Python 3 (3.5 or later)
2. NumPy
3. Matplotlib

## Installation as python PIP package 

Install Topoly using the standard python package installer PIP:

``pip3 install topoly``

Topoly can be installed without administrative privileges in the home folder of a particular user or in a Python
Virtual Environment.
In that case all files (binaries, documentation, libraries and python modules) will be installed in:

``$HOME/.local/``

or ``venv/`` respectively.

If you choose to install Topoly with administrative privileges then everything will be installed in:
`/usr/local/`

Please note that after the installation it is necessary to add the folder that contains libraries

## Installation as DEB, RPM, ZIP

Topoly is also distributed as a DEB, RPM and ZIP package.

DEB and RPM packages install the package to `/usr`, so binaries should be found in `/usr/bin`, libraries in `/usr/lib` 
and the documentation in `/usr/share/doc`

If you choose to install Topoly from a ZIP package please make sure that the libraries from the `lib` subfolder are 
placed in a folder that is listed in the `LD_LIBRARY_PATH`.

The Python wrappers are built as module extensions and therefore they require that the `lib` subfolder should be 
added to your `PYTHONPATH` variable. 

## Testing

To verify that the topoly is correctly installed please run the `runtests.sh` script located in `share/doc/topoly/test`. 
(`/usr/share/doc/topoly/test` if installed from RPM or DEB)


## Using Topoly

Please have a look at the tests in `share/doc/topoly/test` to see usage examples.
or have a look at our test project:

https://github.com/ilbsm/topoly_test

