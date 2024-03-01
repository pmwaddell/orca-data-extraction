#!/usr/bin/env python3
"""
Structures subclasses that represent types of data from ORCA .out file.

The DataSection abstract class provides an interface for creating subclasses
that represent different types of data from an ORCA .out file. These
subclasses use regular expressions to search the contents of the .out file and
find a particular type of data (e.g. input geometry coordinates for a series of
atoms) and then stores these data using an appropriate structure. These
subclasses also have a method to return these data to the user.
"""
__author__ = "Peter Waddell"
__copyright__ = "Copyright 2024"
__credits__ = ["Peter Waddell"]
__version__ = "0.1.0"
__date__ = "2024/02/27"
__maintainer__ = "Peter Waddell"
__email__ = "pmwaddell9@gmail.com"
__status__ = "Prototype"

from abc import ABC, abstractmethod


class DataSection(ABC):
    """
    Searches and stores a particular type of data from an ORCA .out file.

    Attributes
    ----------
    _out_filename : str
        Name of the ORCA .out file that will be searched.
    _outfile_contents : str
        String containing the full text of the ORCA .out file.
    _data : dict
        Dictionary containing the desired data, with relevant categories as
        keys (e.g. atom labels, bond tuples, polarizability parameters, etc.)
        and their corresponding values as values. Conventionally both are strs.

    Methods
    -------
    _find_data
        Searches the .out file for the desired data, which is used to store
        these data in the _data attribute.
    get_data
        Getter method that returns the _data attribute.
    get_datum
        Getter method that returns a 'datum' (one entry in the _data dict).
    get_section_name
        Getter method that returns the name of the DataSection subclass.
    get_out_filename
        Getter method that returns name of the .out file that the data is from.
    """
    # Class attributes.
    _std_error_msg = 'ERROR: not found'

    def __init__(self, out_filename, outfile_contents):
        """
        Parameters
        ----------
        out_filename : str
            Name of the ORCA .out file that will be searched.
        outfile_contents : str
            String containing the full text of the ORCA .out file.
        """
        self._section_name = ''
        self._out_filename = out_filename
        self._outfile_contents = outfile_contents
        self._data = self._find_data()

    @abstractmethod
    def _find_data(self):
        """
        Search the .out file for a set of data, return as dict containing
        relevant categories as keys (e.g. atom labels, bond tuples,
        polarizability parameters, etc.) and their corresponding values
        as values.
        """
        pass

    def get_data(self):
        """
        Getter method that returns the _data attribute.

        Returns
        -------
        dict
            The _data attribute.
        """
        return self._data.copy()

    def get_datum(self, datum_label):
        """
        Return the value associated with a particular key (datum_label) from
        the _data dict attribute.

        Parameters
        ----------
        datum_label : str
            Key for the _data dictionary.

        Returns
        -------
        Value from the _data dictionary corresponding to param.
        """
        try:
            result = self._data[datum_label]
            if type(result) is dict:
                return result.copy()
            else:
                return result
        except KeyError:
            print(f'Error: {datum_label} not found in {self._section_name}.')
            return None

    def get_section_name(self):
        """
        Getter method that returns the _section_name attribute.

        Returns
        -------
        str
            _section_name attribute.
        """
        return self._section_name

    def get_out_filename(self):
        """
        Returns string of the filename of the ORCA .out file associated
        with this instance.

        Returns
        -------
        str
            String of the filename of the ORCA .out file.
        """
        return self._out_filename
