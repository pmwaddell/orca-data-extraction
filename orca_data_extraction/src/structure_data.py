#!/usr/bin/env python3
"""
Provides the StructureData class for use with other scripts.

The StructureData class holds information from an ORCA .out file,
as specified by an input .txt file. It holds these data in a dictionary
with the names of data sections as keys and corresponding DataSection
subclasses as values. It contains methods to get data from these sections.
"""
__author__ = "Peter Waddell"
__copyright__ = "Copyright 2024"
__credits__ = ["Peter Waddell"]
__version__ = "0.1.1"
__date__ = "2024/12/30"
__maintainer__ = "Peter Waddell"
__email__ = "pmwaddell9@gmail.com"
__status__ = "Prototype"


class StructureData:
    """
    Associates a desired subset of data from an ORCA .out file.

    Attributes
    ----------
    __out_filename : str
        String of the filename of the ORCA .out file this object
        represents.
    __input_filename : str
        String of filename of .txt file that contains lists of desired atom
        labels for each type of data that will be pulled from the .out file.
    __data_sections : dict
        Dictionary mapping strings of the names of DataSection subclasses to
        instances those subclasses associated with this .out file.

    Methods
    -------
    __read_file
        Converts a text file to a single string using .read().
    __check_coord_system
        Determines whether the coordinate system was set up correctly.
    get_out_filename
        Gives the filename of the .out file from which the data was taken.
    get_input_filename
        Gives the filename of the input .txt file.
    get_std_error_msg
        Gives the standard error message used by this class.
    get_data_sections
        Gives __data_sections attribute, a dictionary that maps names of
        DataSection subclasses to their corresponding instances.
    get_data_section
        Gives a DataSection subclass (value) from the __data_sections dict
        given its name (key).
    get_data_section_data
        Gives dict containing the data from a particular DataSection subclass
        instance.
    get_data_section_datum
        Gives 'datum' (value from DataSection subclass data dictionary)
        corresponding to a given label (key for said dict).
    """
    # Class attributes.
    __std_error_msg = 'ERROR: not found'

    def __init__(self, out_filename, input_filename, data_sections):
        """
        Parameters
        ----------
            out_filename : str
                String of filename of .out file this object represents.
            input_filename : str
                String of filename of .txt file that contains lists of desired
                atom labels for each type of data that will be pulled from the
                .out file.
        """
        self.__out_filename = out_filename
        self.__input_filename = input_filename
        self.__data_sections = data_sections

    def get_out_filename(self):
        """
        Gives the filename of the .out file from which the data was taken.

        Returns
        -------
        str
            __out_filename attribute.
        """
        return self.__out_filename

    def get_input_filename(self):
        """
        Gives the filename of the input .txt file.

        Returns
        -------
        str
            __input_filename attribute.
        """
        return self.__input_filename

    # Results/data:
    @staticmethod
    def get_std_error_msg():
        """
        Gives the standard error message used by this class.

        Returns
        -------
        str
            __std_error_msg attribute.
        """
        return StructureData.__std_error_msg

    def get_data_sections(self):
        """
        Gives __data_sections attribute, a dictionary that maps names of
        DataSection subclasses to their corresponding instances.

        Returns
        -------
        dict
            __data_sections attribute.
        """
        return self.__data_sections.copy()

    def get_data_section(self, section_name):
        """
        Gives a DataSection subclass (value) from the __data_sections dict
        given its name (key).

        Parameters
        ----------
        section_name : str
            Name of a DataSection subclass.

        Returns
        -------
        DataSection subclass
            Instance of a DataSection subclass corresponding to the passed name.
        """
        try:
            return self.__data_sections[section_name]
        except KeyError:
            return f'ERROR: Data section {section_name} not found in ' \
                   f'{self.get_input_filename()} (input file).'

    def get_data_section_data(self, section_name):
        """
        Gives dict containing the data from a particular DataSection subclass
        instance.

        Parameters
        ----------
        section_name : str
            Name of the DataSection, should be a key in __data_sections
            attribute.

        Returns
        -------
        dict
            Data found by a DataSection subclass instance.
        """
        try:
            return self.get_data_section(section_name).get_data()
        except AttributeError:
            return f'ERROR: Data section {section_name} not found in ' \
                   f'{self.get_input_filename()} (input file).'

    def get_data_section_datum(self, section_name, datum_label):
        """
        Gives 'datum' (value from DataSection subclass data dictionary)
        corresponding to a given label (key for said dict).

        Parameters
        ----------
        section_name : str
            Name of the DataSection, should be a key in __data_sections
            attribute.
        datum_label : str or tuple
            Key to the DataSection subclass data dictionary for the desired
            datum.

        Returns
        -------
        str or dict
            'Datum' corresponding to the datum label key in the DataSection
            data dictionary.
        """
        try:
            return self.get_data_section(section_name).get_datum(datum_label)
        except AttributeError:
            return f'ERROR: Data section {section_name} not found in ' \
                   f'{self.get_input_filename()} (input file).'
