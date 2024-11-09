#!/usr/bin/env python3
"""
The LoewdinChargeSums class searches for and stores sums of Loewdin charges 
from an ORCA .out file.

The LoewdinCharges class searches for the Loewdin charge data for a series of
atoms from a ORCA .out file, as specified by input (tuple of) tuples which
contains a series of LEXICOGRAPHICALLY SORTED atom labels to search for.
"""
__author__ = "Peter Waddell"
__copyright__ = "Copyright 2024"
__credits__ = ["Peter Waddell"]
__version__ = "0.1.0"
__date__ = "2024/02/27"
__maintainer__ = "Peter Waddell"
__email__ = "pmwaddell9@gmail.com"
__status__ = "Prototype"

from orca_data_extraction.src.data_section_with_inputs import DataSectionWithInputs
from orca_data_extraction.src.loewdin_charges import LoewdinCharges


class LoewdinChargeSums(DataSectionWithInputs):
    """
    Finds and stores Loewdin charge sum data from a ORCA .out file.

    Methods
    -------
    _search
        Search the .out file for Loewdin charge sum data.
    get_datum
        Gives the sum of Loewdin charges from _data for a set of atoms.
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
            Tuple of tuples of atom labels (e.g. ('1 H', '0 O) for which
            Loewdin charge sum data will be searched and then summed.
        """
        super().__init__(out_filename, outfile_contents, inputs)
        self._section_name = 'Loewdin Charge Sums'

    def _search(self, atoms_tuple):
        """
        Use regex to search .out file to get an Loewdin charge sum.

        Parameters
        ----------
        atoms_tuple : tuple
            Tuple of the atom labels for which an Loewdin charge sum will be
            calculated.

        Returns
        -------
        str
            A string of the sum of Loewdin charges of atoms corresponding to
            the atom labels in the aforementioned tuple.

        # TODO: does this part of the docstring need fixing??
        Raises
        ------
        TypeError
            This occurs when the regex (from the associated LoewdinCharges
            instance) fails to find what it is looking for.
        """
        loewdin_charges = LoewdinCharges(
            self._out_filename, self._outfile_contents, atoms_tuple
        )
        charge_sum = 0
        for atom_label in atoms_tuple:
            try:
                charge_sum += float(loewdin_charges.get_datum(atom_label))
            except TypeError:
                print(f'Error: {atom_label} not found in {self._out_filename} '
                      f'({loewdin_charges.get_section_name()}) during attempt '
                      f'to sum charges.')
                return None
        return str(round(charge_sum, 5))

    def get_datum(self, atoms_tuple):
        """
        Gives the sum of Loewdin charges from _data for a set of atoms.

        Parameters
        ----------
        atoms_tuple : tuple
            A tuple containing strings of the desired atom labels.

        Returns
        -------
        str
            String consisting of the sum of Loewdin charges of the atoms in
            atoms_tuple.

        Raises
        ------
        KeyError
            This occurs when the input atoms tuple can't be found as a key in
            the dict containing the Loewdin charge sum data.
        """
        # So, we need to account for the possibility that the atoms in the
        # tuple "atoms" will be in a different order compared to how they are
        # in "inputs", which is lexicographically sorted. Therefore, the
        # "atoms" tuple must be sorted before searching the _data dict.
        try:
            return self._data[tuple(sorted(list(atoms_tuple)))]
        except KeyError:
            print(f'ERROR: {atoms_tuple} not found in {self._out_filename} '
                  f'(Loewdin Charge Sums).')
            return None
