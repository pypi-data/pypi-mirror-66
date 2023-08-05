# README

This package is meant to help users process their rheology data into an HDF5 file that can be
uploaded to the [Materials Data Facility](https://materialsdatafacility.org/).  The rheodata package
contains `extractors` that are instrument specific.  Currently the list of supported extractors are:

* Anton Paar MCR302

The package also contains a `data_converter` file that will take the raw and parsed data from the extractors
and convert them into a single HDF5 file.  One can also add metadata to the overall project and to individual
tests.

To install the package, clone the repo and navigate to the downloaded folder in your command line.  Once
there run:

`pip install .`

Later this package will be uploaded to PyPi
    