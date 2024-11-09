#!/usr/bin/env python3
"""
The BondLengths class calculates or searches for and stores bond length data
from an ORCA .out file.
"""
__author__ = "Peter Waddell"
__copyright__ = "Copyright 2024"
__credits__ = ["Peter Waddell"]
__version__ = "0.1.0"
__date__ = "2024/02/27"
__maintainer__ = "Peter Waddell"
__email__ = "pmwaddell9@gmail.com"
__status__ = "Prototype"

import math

from orca_data_extraction.src.data_section_with_inputs import DataSectionWithInputs
from orca_data_extraction.src.final_geom import FinalGeometry


class BondLengths(DataSectionWithInputs):
    """
    Finds and stores bond length data from an ORCA .out file.

    Methods
    -------
    _search
        Search the .out file for bond length data.
    __calc_atom_angle
        Manually calcs the "bond length" of the 2 atoms in the input bond tuple.
    get_datum
        Gives the bond length from _data for a certain bond.
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
            Tuple of 'bond tuples' (i.e. tuples of two strings of atom labels,
            e.g. ('1 H', '0 O')) for which bond length data will be searched.
        """
        super().__init__(out_filename, outfile_contents, inputs)
        self._section_name = 'Bond Lengths'

    def _search(self, bond_tuple):
        return self.__calc_atom_distance(bond_tuple)

    def __calc_atom_distance(self, bond_tuple):
        """
        Manually calcs the distance between two atoms in the input bond tuple.

        Of course, these can be any two atoms whose coordinates appear in the
        .out file; they do not have to be bound to each other in any way.

        Parameters
        ----------
        bond_tuple : tuple
            Tuple containing two atom labels, representing the desired bond.

        Returns
        -------
        str
            String containing the distance between the two atoms in Angstroms,
            as calculated from sqrt((x1-x2)^2 + (y1-y2)^2 + (z1-z2)^2).

        Raises
        ------
        TypeError
            This occurs when one of the atom labels in the input bond tuple
            does not have corresponding data in _input_geoms.
        """
        final_geom = \
            FinalGeometry(out_filename=self._out_filename,
                          outfile_contents=self._outfile_contents,
                          inputs=(bond_tuple[0], bond_tuple[1]))

        atom0, atom1 = bond_tuple[0], bond_tuple[1]
        # I've decided DRY here is more trouble than its worth...
        try:
            atom0_x = float(final_geom.get_datum(atom0)['x'])
            atom0_y = float(final_geom.get_datum(atom0)['y'])
            atom0_z = float(final_geom.get_datum(atom0)['z'])
        except TypeError:
            print(f'Manual calculation failed for bond {atom0}-{atom1}:'
                  f'{atom0} geometry data not found.')
            return None
        try:
            atom1_x = float(final_geom.get_datum(atom1)['x'])
            atom1_y = float(final_geom.get_datum(atom1)['y'])
            atom1_z = float(final_geom.get_datum(atom1)['z'])
        except TypeError:
            print(f'Manual calculation failed for bond {atom0}-{atom1}:'
                  f'{atom1} geometry data not found.')
            return None
        return str(
            round(math.sqrt(((atom0_x - atom1_x) ** 2) +
                             ((atom0_y - atom1_y) ** 2) +
                             ((atom0_z - atom1_z) ** 2)), 5)
        )

    def get_datum(self, bond_tuple):
        """
        Gives the bond length from _data for a certain bond.

        Parameters
        ----------
        bond_tuple : tuple
            Tuple containing two atom labels, representing the desired bond.

        Returns
        -------
        str
            String consisting of the length of the corresponding
            bond in Angstroms.

        Raises
        ------
        KeyError
            This occurs when the input 'bond' tuple can't be found as a key in
            the dict containing the bond length data.
        """
        # In order to find the bond length no matter which atom is listed first
        # in the bond tuple, this override is necessary.
        try:
            return self._data[bond_tuple]
        except KeyError:
            try:
                flipped_bond_tuple = (bond_tuple[1], bond_tuple[0])
                return self._data[flipped_bond_tuple]
            except KeyError:
                print(f'ERROR: {bond_tuple} not found in '
                      f'{self._out_filename} (Bond Lengths).')
                return None
