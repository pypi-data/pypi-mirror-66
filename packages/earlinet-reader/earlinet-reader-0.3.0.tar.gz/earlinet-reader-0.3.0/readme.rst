EARLINET file reader
====================

This package provides utilities to handle processed lidar data in one of EARLINET's NetCDF formats. Currently
it supports low-temporal-resolution files from EARLINET's Single Calculus Chain pre-processor and files with
aerosol optical properties.

Installation
------------

You can install the package using the ``pip`` command::

   pip install earlinet-reader

You can also install also directly from the `source code <http://bitbucket.org/iannis_b/earlinet-reader/src>`_. You should extract the code in a folder (e.g. ``earlinet-reader``)
and then run::

   pip install ./earlinet-reader

Command line interface for ELPP files
-------------------------------------

The main way of using this package, is through the command line interface program called ``plotELPP``.

The usage of the ``plotELPP`` program is described bellow::

   usage: plotELPP [-h] [--vmin VMIN] [--vmax VMAX] [-v VARIABLE] [--log]
                   [--normalize] [--normmin NORMMIN] [--normmax NORMMAX] [--grid]
                   [--dpi DPI] [--errorevery ERROREVERY] [--html] [-d] [-s]
                   file_patter [rmin] [rmax]

   Command line tool to plot lidar pre-processed files from the SCC's ELPP.

   positional arguments:
     file_patter           The path to a file (possibly including glob patterns).
     rmin                  Minimum range to plot (in km)
     rmax                  Maximum range to plot (in km)

   optional arguments:
     -h, --help            show this help message and exit
     --vmin VMIN           Minimum variable value to plot
     --vmax VMAX           Maximum variable value to plot
     -v VARIABLE, --variable VARIABLE
                           Name of variable to plot
     --log                 Plot log10 values of variable.
     --normalize           Normalize variables on molecular signal
     --normmin NORMMIN     If nomralize is selected, the minimum altitude for
                           normalization (in km).
     --normmax NORMMAX     If nomralize is selected, the maximum altitude for
                           normalization (in km).
     --grid                Show grid on the plots
     --dpi DPI             DPI of the output image
     --errorevery ERROREVERY
                           Plot error bar only every x points.
     --html                Create an HTML report.
     -d, --debug           Print dubuging information.
     -s, --silent          Show only warning and error messages.

For example, let's assume you want to plot the content of the file ``20170216oh00_584.nc``.

* You can plot a single variable in the file using::

   plotELPP 20170216oh00_584.nc --variable elPR

* You can specify the minimum and maxi,um range of the plots e.g. from 0 to 5 km::

   plotELPP 20170216oh00_584.nc 0 5 --variable elPR

* You can tune few plotting parameters: turn the grid on and choose the output dpi::

   plotELPP 20170216oh00_584.nc --variable elPR --grid --dpi 200

* If you omit the variable parameter, you can show all variables in the netCDF file on a single plot::

   plotELPP 20170216oh00_584.nc

* You can see more info about the file by choosing the ``--html`` option::

   plotELPP 20170216oh00_584.nc --html

* You can perform the above operations for multiple files at once using ``*`` and ``?`` as wildcards::

   plotELPP `20170216oh00_*.nc` --html


Command line interface for optical property files
-------------------------------------------------
You can plot files containing aerosol optical properties usign the commnad ``plotoptical``. The usage is similar
to the ``plotELPP`` program::

   usage: plotoptical [-h] [-v VARIABLE] [--grid] [--dpi DPI]
                      [--errorevery ERROREVERY] [--html] [-d] [-s]
                      file_patter [zmin] [zmax]

   Command line tool to plot lidar optical property files.

   positional arguments:
     file_patter           The path to a file (possibly including glob patterns).
     zmin                  (optional) Minimum altitude asl to plot (in km)
     zmax                  (optional) Maximum altitude asl to plot (in km)

   optional arguments:
     -h, --help            show this help message and exit
     -v VARIABLE, --variable VARIABLE
                           Name of variable to plot
     --grid                Show grid on the plots
     --dpi DPI             DPI of the output image
     --errorevery ERROREVERY
                           Plot error bar only every x points.
     --html                Create an HTML report.
     -d, --debug           Print dubuging information.
     -s, --silent          Show only warning and error messages.

Converting calibrated HiRELPP files to GEOMS format
---------------------------------------------------
HiRELPP files can converted to GEOMS format, using the appropriate method::

   from earlinet_reader import hirelpp_files
   h = hirelpp_files.HiRElPPFile(<path_to_hirelpp_file>)
   h.convert_to_geoms(location, affiliation)

The `location` and `affiliation` arguments are used to create the correcte GEOMS filename.
Location should be a string describing the lidar location e.g. `bucharest`. Affiliation
should be the institue acronym, e.g. `inoe`. If omitted, the `affiliation` value will be
inferred from HiRELPP properties.

Reporting bugs
--------------
If want to report a bug, ask for a new feature, or have an idea for an improvement fell free to contribute it through
the `bug tracking system <https://bitbucket.org/iannis_b/earlinet-reader/issues>`_.


