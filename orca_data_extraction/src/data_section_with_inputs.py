#!/usr/bin/env python3
"""
An abstract class for DataSection subclasses that need to take inputs.

Inputs (e.g. tuples of strings of atom labels, or tuples of tuples of atom
labels) specify which pieces of data should be searched for. The result of
the search is a dictionary with each element from the inputs as keys and the
resulting data from the search as values.
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

from orca_data_extraction.src.data_section import DataSection


class DataSectionWithInputs(DataSection, ABC):
    """
    A subclass of DataSection for data that takes a set of inputs to search for.

    Attributes
    ----------
    _inputs : tuple
        A tuple of information (e.g. strings of atom labels, or of tuples that
        contain strings of atom labels) which signify which pieces of
        information should be searched for.

    Methods
    -------
    _find_data
        Searches the .out file for the desired data, which is used to store
        these data in the _data attribute.
    _search
        Abstract method which defines how each subclass of this class should
        go about searching the .out file for its particular type of data.
    get_inputs
        Returns a copy of the _inputs attribute.
    """
    def __init__(self, out_filename, outfile_contents, inputs):
        """
        Parameters
        ----------
        out_filename : str
            Name of the ORCA .out file that will be searched.
        outfile_contents : str
            String containing the full text of the ORCA .out file.
        inputs : tuple
            A tuple of information (e.g. strings of atom labels, or of tuples
            that contain strings of atom labels) which signify which pieces of
            information should be searched for.
        """
        self._inputs = inputs
        super().__init__(out_filename, outfile_contents)

    def _find_data(self):
        """
        For each element in _inputs, perform a regex search (via _search) of
        the .out file and find the desired data.

        Returns
        -------
        search_results : dict
            A dictionary containing the elements from _inputs as keys and the
            result of the regex searches as values.
        """
        search_results = {}
        for elem in self._inputs:
            search_results[elem] = self._search(elem)
        return search_results

    @abstractmethod
    def _search(self, elem):
        """
        Use regular expressions to search the .out file for some data, as
        specified by elem, and return it.

        Parameters
        ----------
        elem
            Element from _inputs, generally either a string or tuple of strings.
        """
        pass

    def get_inputs(self):
        """
        Returns the inputs used for this instance.

        Returns
        -------
        tuple
            _inputs attribute.
        """
        return self._inputs

