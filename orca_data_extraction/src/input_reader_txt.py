#!/usr/bin/env python3
"""
The InputReaderTxt class finds and stores input info for DataSection subclasses.

The InputReaderTxt class searches for the "inputs" from an input .txt file to be
used in the instantiation of various subclasses of the DataSection class,
for example: FinalGeometry, MullikenCharges, BondLengths, and BondAngles. It
also determines whether the user wants to skip any of these sections, as
indicated when the corresponding line in the input .txt file is left blank.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
NOTE: reading inputs from .txt files is currently deprecated.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

"""
__author__ = "Peter Waddell"
__copyright__ = "Copyright 2024"
__credits__ = ["Peter Waddell"]
__version__ = "0.1.1"
__date__ = "2024/12/30"
__maintainer__ = "Peter Waddell"
__email__ = "pmwaddell9@gmail.com"
__status__ = "Prototype"

from orca_data_extraction.src.input_reader import InputReader


class InputReaderTxt(InputReader):
    """
    Finds/stores inputs for DataSection subclasses from structured .txt file.

    Attributes
    ----------
    __input_filename: str
        String of filename of .txt file that contains lists of desired atom
        labels for each type of data that will be pulled from the .out file.
    __input_contents : lst
        List containing a series of strings, one for each line in the given
        input .txt file.
    __initial_geom_inputs : tuple
        Tuple of atom labels for which initial geometry data will be searched.
    __final_geom_inputs : tuple
        Tuple of atom labels for which final geometry data will be searched.
    __bond_length_inputs : tuple
        Tuple of 'bond tuples' (i.e. tuples of two strings of atom labels,
        e.g. ('0 P', '1 C')) for which bond length data will be searched.
        These need to be tuples because they are hashed later on.
    __bond_angle_inputs : tuple
        Tuple of 'angle tuples' (i.e. tuples of three strings of atom labels,
        e.g. ('0 P', '1 C', '2 C')) for which bond angle data will be searched.
        These need to be tuples because they are hashed later on.
    __mulliken_charge_inputs : tuple
        Tuple of atom labels for white Mulliken charge data will be searched.
    __mulliken_charge_sum_inputs : tuple
        Tuple of tuples of atom lables whose Mulliken charges will be summed.
    __loewdin_charge_inputs : tuple
        Tuple of atom labels for white Loewdin charge data will be searched.
    __loewdin_charge_sum_inputs : tuple
        Tuple of tuples of atom lables whose Loewdin charges will be summed.

    Methods
    -------
    __readlines_file
        Converts a text file to a list of strings, one for each line,
        using .readlines().
    __read_inputs_atoms
        Returns list of input parameters from a given line in input .txt file.
        Used for lines that contain a list of atom labels.
    __read_inputs_bonds
        Returns list of input parameters from a given line in input .txt file.
        Used for lines that contain a list of bond labels.
    __read_initial_geom
        Retrieves the desired atom labels from the input .txt file for
        initial geometry.
    __read_final_geom
        Retrieves the desired atom labels from the input .txt file for
        final geometry.
    __read_bond_length
        Retrieves the desired sets of atom labels ('bond tuples') from the
        input .txt file for bond lengths.
    __read_bond_angle
        Retrieves the desired sets of atom labels ('angle tuples') from the
        input .txt file for bond angles.
    __read_mulliken_charge
        Retrieves the desired set of atom labels from the input .txt file for
        Mulliken charges.
    __read_mulliken_charge_sum
        Retrieves the desired set of atom labels ('atom tuples') from the input
        .txt file for Mulliken charge sums.
    __read_loewdin_charge
        Retrieves the desired set of atom labels from the input .txt file for
        Loewdin charges.
    __read_lowedin_charge_sum
        Retrieves the desired set of atom labels ('atom tuples') from the input
        .txt file for Loewdin charge sums.
    get_initial_geom_inputs
        Returns tuple of initial geometry inputs.
    get_final_geom_inputs
        Returns tuple of final geometry inputs.
    get_bond_length_inputs
        Returns tuple of bond len. inputs ('bond tuples').
    get_bond_angle_inputs
        Returns tuple of bond angle inputs ('angle tuples').
    get_mulliken_charge_inputs
        Returns tuple of Mulliken charge inputs.
    get_mulliken_charge_sum_inputs
        Returns tuple of Mulliken charge sum inputs.
    get_loewdin_charge_inputs
        Returns tuple of Loewdin charge inputs.
    get_loewdin_charge_sum_inputs
        Returns tuple of Loewdin charge sum inputs.
    """
    def __init__(self, input_filename):
        """
        Parameters
        ----------
        input_filename : str
            String of filename of .txt file that contains lists of desired atom
            labels for each type of data that will be pulled from the .out file.
        """
        super().__init__(input_filename)

        self.__input_contents = self.__readlines_file(self.__input_filename)

        # Read the values for input attributes from the input text file.
        self.__initial_geom_inputs = self.__read_initial_geom()
        self.__final_geom_inputs = self.__read_final_geom()
        self.__bond_length_inputs = self.__read_bond_length()
        self.__bond_angle_inputs = self.__read_bond_angle()
        self.__mulliken_charge_inputs = self.__read_mulliken_charge()
        self.__mulliken_charge_sum_inputs = self.__read_mulliken_charge_sum()
        self.__loewdin_charge_inputs = self.__read_loewdin_charge()
        self.__loewdin_charge_sum_inputs = self.__read_loewdin_charge_sum()
        # TODO: I'm thinkin of holding these in a dictionary like StructureData now does

    @staticmethod
    def __readlines_file(f):
        """
        Converts a text file to a list of strings, one for each line,
        using .readlines().

        Parameters
        ----------
        f : str
            Filename of the desired file to read.

        Returns
        -------
        contents : lst
            List of strings, one for each line of text in the file.

        Raises
        ------
        FileNotFoundError
            If f is not the filename of a file in the current directory.
        """
        try:
            with open(f) as file_object:
                contents = file_object.readlines()
        except FileNotFoundError:
            print("File not found")
        else:
            file_object.close()
            return contents

    def __read_inputs_atoms(self, line_num):
        """
        Returns tuple of input parameters from a given line in input .txt file.
        Used for lines that contains a series of atom labels: e.g. P1,P2,N5 etc.

        Parameters
        ----------
        line_num : int
            Number of the desired line.

        Returns
        -------
        tuple
            Tuple of list that results from splitting the specified line in the
            input .txt file, using a comma as the separator.
        """
        result = []
        for count, line in enumerate(self.__input_contents):
            if count == line_num:
                result = line.strip().split(',')
        if result == ['']:
            return []
        return tuple(result)

    def __read_inputs_lists(self, line_num):
        """
        Returns tuple of tuples of input parameters from a given line in input
        .txt file.
        Used for lines that contain lists of labels:
        e.g. (0 P,1 C);(2 H,3 B) etc.

        Parameters
        ----------
        line_num : int
            Number of the desired line.

        Returns
        -------
        tuple
            Tuple of tuples that results from splitting the specified line in
            the input .txt file, using a semicolon as the separator, and
            removing the parentheses.
        """
        result = []
        for count, line in enumerate(self.__input_contents):
            if count == line_num:
                temp = line.strip().split(';')
                for elem in temp:
                    if elem:
                        result.append(tuple(elem[1:-1].split(',')))
        if result == [()]:
            return []
        return tuple(result)

    def __read_inputs_lists_sort(self, line_num):
        """
        Returns tuple of SORTED tuples of input parameters from a given line in
        input .txt file.

        Used for lines that contain lists of items that can be sorted
        without causing major problems. The reason one would want to do this is
        to reduce ambiguity in future function calls, so that e.g. the atom
        labels could be supplied in any order and the same entry would be found.

        Parameters
        ----------
        line_num : int
            Number of the desired line.

        Returns
        -------
        Tuple
            Tuple of sorted tuples that results from splitting the specified
            line in the input .txt file, using a semicolon as the separator,
            and removing the parentheses.
        """
        result = []
        for count, line in enumerate(self.__input_contents):
            if count == line_num:
                temp = line.strip().split(';')
                for elem in temp:
                    if elem:
                        elem_lst = sorted(elem[1:-1].split(','))
                        result.append(tuple(elem_lst))
        if result == [()]:
            return []
        return tuple(result)

    def __read_initial_geom(self):
        """
        Retrieves the desired atom labels from the input .txt file for
        initial (i.e., user-input) geometry.

        If the line is blank in the input .txt file (meaning this section should
        be skipped for this run of the script), this returns [''].

        Returns
        -------
        lst
            List of atom labels for which initial geom. data will be searched.
        """
        return self.__read_inputs_atoms(4)

    def __read_final_geom(self):
        """
        Retrieves the desired atom labels from the input .txt file for the
        final (e.g., after geometry optimization) geometry.

        If the line is blank in the input .txt file (meaning this section should
        be skipped for this run of the script), this returns [''].

        Returns
        -------
        lst
            List of atom labels for which final geometry data will be searched.
        """
        return self.__read_inputs_atoms(7)

    def __read_bond_length(self):
        """
        Retrieves the desired sets of atom labels ('bond tuples') from the input
        .txt file for bond lengths.

        If the line is blank in the input .txt file (meaning this section should
        be skipped for this run of the script), this returns [()].

        Returns
        -------
        lst
            List of 'bond tuples' (i.e. tuples of two strings of atom labels,
            e.g. ('0 P', '1 C') for which bond length data will be searched or
            calculated. These need to be tuples because they are hashed later.
        """
        return self.__read_inputs_lists(10)

    def __read_bond_angle(self):
        """
        Retrieves the desired sets of atom labels ('angle tuples') from the
        input .txt file for bond angles.

        If the line is blank in the input .txt file (meaning this section should
        be skipped for this run of the script), this returns [()].

        Returns
        -------
        lst
            List of 'angle tuples' (i.e. tuples of three strings of atom labels,
            e.g. ('0 P', '1 C', '2 C') for which bond angle data will be searched
            or calculated. These need to be tuples bc they are hashed later.
        """
        return self.__read_inputs_lists(13)

    def __read_mulliken_charge(self):
        """
        Retrieves the desired atom labels from the input .txt file for
        Mulliken charges.

        If the line is blank in the input .txt file (meaning this section should
        be skipped for this run of the script), this returns [''].

        Returns
        -------
        lst
            List of atom labels for which Mulliken charge data will be searched.
        """
        return self.__read_inputs_atoms(16)

    def __read_mulliken_charge_sum(self):
        """
        Retrieves the desired atom labels from the input .txt file for
        Mulliken charge sum calculation.

        If the line is blank in the input .txt file (meaning this section should
        be skipped for this run of the script), this returns [''].

        Returns
        -------
        lst
            List of atom labels for which Mulliken charge sum data will
            be calculated.
        """
        return self.__read_inputs_lists_sort(19)

    def __read_loewdin_charge(self):
        """
        Retrieves the desired atom labels from the input .txt file for
        Loewdin charges.

        If the line is blank in the input .txt file (meaning this section should
        be skipped for this run of the script), this returns [''].

        Returns
        -------
        lst
            List of atom labels for which Loewdin charge data will be searched.
        """
        return self.__read_inputs_atoms(22)

    def __read_loewdin_charge_sum(self):
        """
        Retrieves the desired atom labels from the input .txt file for
        Loewdin charge sum calculation.

        If the line is blank in the input .txt file (meaning this section should
        be skipped for this run of the script), this returns [''].

        Returns
        -------
        lst
            List of atom labels for which Loewdin charge sum data will
            be calculated.
        """
        return self.__read_inputs_lists_sort(25)

    # Getter/selector methods:
    def get_initial_geom_inputs(self):
        """
        Returns tuple of initial geometry inputs.

        Returns
        -------
        tuple
            __initial_geom_inputs attribute.
        """
        return self.__initial_geom_inputs

    def get_final_geom_inputs(self):
        """
        Returns tuple of final geometry inputs.

        Returns
        -------
        tuple
            __final_geom_inputs attribute.
        """
        return self.__final_geom_inputs

    def get_bond_length_inputs(self):
        """
        Returns tuple of bond length inputs.

        Returns
        -------
        tuple
            __bond_length_inputs attribute.
        """
        return self.__bond_length_inputs

    def get_bond_angle_inputs(self):
        """
        Returns tuple of bond angle inputs.

        Returns
        -------
        tuple
            __bond_angle_inputs attribute.
        """
        return self.__bond_angle_inputs

    def get_mulliken_charge_inputs(self):
        """
        Returns tuple of Mulliken charge inputs.

        Returns
        -------
        tuple
            __mulliken_charge_inputs attribute.
        """
        return self.__mulliken_charge_inputs

    def get_mulliken_charge_sum_inputs(self):
        """
        Returns tuple of Mulliken charge sum inputs.

        Returns
        -------
        tuple
            __mulliken_charge_inputs attribute.
        """
        return self.__mulliken_charge_sum_inputs

    def get_loewdin_charge_inputs(self):
        """
        Returns tuple of Loewdin charge inputs.

        Returns
        -------
        tuple
            __loewdin_charge_inputs attribute.
        """
        return self.__loewdin_charge_inputs

    def get_loewdin_charge_sum_inputs(self):
        """
        Returns tuple of Loewdin charge sum inputs.

        Returns
        -------
        tuple
            __loewdin_charge_sum_inputs attribute.
        """
        return self.__loewdin_charge_sum_inputs
