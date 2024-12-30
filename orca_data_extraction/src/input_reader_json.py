#!/usr/bin/env python3
"""
InputReaderJSON finds and stores input info for DataSection subclasses.

The InputReaderJSON class searches for the "inputs" from an input JSON file to
be used in the instantiation of various subclasses of the DataSection class,
for example: FinalGeometry, MullikenCharges, BondLengths, and BondAngles. It
also determines whether the user wants to skip any of these sections, as
indicated by an empty list in the JSON file.
"""
__author__ = "Peter Waddell"
__copyright__ = "Copyright 2024"
__credits__ = ["Peter Waddell"]
__version__ = "0.1.0"
__date__ = "2024/12/30"
__maintainer__ = "Peter Waddell"
__email__ = "pmwaddell9@gmail.com"
__status__ = "Prototype"

import json

from orca_data_extraction.src.input_reader import InputReader


class InputReaderJSON(InputReader):
    """
    Finds/stores inputs for DataSection subclasses from a JSON file.

    Attributes
    ----------
    _input_filename: str
        String of filename of .txt file that contains lists of desired atom
        labels for each type of data that will be pulled from the .out file.
    _inputs_dict: dict
        Dictionary containing the information from the JSON inputs file.

    Methods
    -------
    __make_inputs_dict
        Reads the JSON input file and converts the information therein
        to a dict.
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
            String of filename of JSON file that contains lists of desired atom
            labels for each type of data that will be pulled from the .out file.
        """
        super().__init__(input_filename)
        self._inputs_dict = self.__make_inputs_dict()

    def __make_inputs_dict(self):
        """
        Returns a dictionary from JSON inputs file.

        Returns
        -------
        dict
            Dictionary from JSON inputs file.
        """
        with open(self._input_filename) as json_file:
            inputs_dict = json.load(json_file)

        for key in inputs_dict.keys():
            inputs = inputs_dict[key]
            for i, elem in enumerate(inputs):
                if type(elem) is list:
                    if key == "bond_angle_data_labels":
                        inputs[i] = tuple(elem)
                    else:
                        inputs[i] = tuple(sorted(elem))
            inputs_dict[key] = tuple(inputs)

        return inputs_dict

    # Getter/selector methods:
    def get_initial_geom_inputs(self):
        """
        Returns tuple of initial geometry inputs.

        Returns
        -------
        tuple
            Tuple of initial geometry inputs.
        """
        return self._inputs_dict['initial_geometry_atom_labels']

    def get_final_geom_inputs(self):
        """
        Returns tuple of final geometry inputs.

        Returns
        -------
        tuple
            Tuple of final geometry inputs.
        """
        return self._inputs_dict['final_geometry_atom_labels']

    def get_bond_length_inputs(self):
        """
        Returns tuple of bond length inputs.

        Returns
        -------
        tuple
            Tuple of bond length inputs.
        """
        return self._inputs_dict['bond_length_data_labels']

    def get_bond_angle_inputs(self):
        """
        Returns tuple of bond angle inputs.

        Returns
        -------
        tuple
            Tuple of bond angle inputs.
        """
        return self._inputs_dict['bond_angle_data_labels']

    def get_mulliken_charge_inputs(self):
        """
        Returns tuple of Mulliken charge inputs.

        Returns
        -------
        tuple
            Tuple of Mulliken charge inputs.
        """
        return self._inputs_dict['mulliken_charge_atom_labels']

    def get_mulliken_charge_sum_inputs(self):
        """
        Returns tuple of Mulliken charge sum inputs.

        Returns
        -------
        tuple
            Tuple of Mulliken charge sum inputs.
        """
        return self._inputs_dict['mulliken_charge_sum_atom_label_lists']

    def get_loewdin_charge_inputs(self):
        """
        Returns tuple of Loewdin charge inputs.

        Returns
        -------
        tuple
            Tuple of Loewdin charge inputs.
        """
        return self._inputs_dict['loewdin_charge_atom_labels']

    def get_loewdin_charge_sum_inputs(self):
        """
        Returns tuple of Loewdin charge sum inputs.

        Returns
        -------
        tuple
            Tuple of Loewdin charge sum inputs.
        """
        return self._inputs_dict['loewdin_charge_sum_label_lists']
