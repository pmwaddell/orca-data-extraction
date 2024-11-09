#!/usr/bin/env python3
"""
The BondAngles class calculates or searches for and stores bond angle data from
an ORCA .out file.
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


class BondAngles(DataSectionWithInputs):
    """
    Finds and stores bond angle data from an ORCA .out file.

    Methods
    -------
    _search
        Search the .out file for bond angle data.
    __calc_atom_angle
        Manually calcs the "bond angle" of the 3 atoms in the input angle tuple.
    get_datum
        Gives the bond angle from _data for a certain bond.
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
            Tuple of 'angle tuples' (i.e. tuples of three strings of atom
            labels, e.g. ('1 H', '0 O', '2 H')) for which data will be searched.
        """
        super().__init__(out_filename, outfile_contents, inputs)
        self._section_name = 'Bond Angles'

    def _search(self, angle_tuple):
        return self.__calc_atom_angle(angle_tuple)

    def __calc_atom_angle(self, angle_tuple):
        """
        Manually calcs the "bond angle" of the 3 atoms in the input angle_tuple.

        Of course, these can be any three atoms whose coordinates appear in the
        .out file, they do not have to be classified as having a "bond angle"
        by ORCA.

        Parameters
        ----------
        angle_tuple : tuple
            Tuple containing three atom labels, representing the desired bond.

        Returns
        -------
        str
            String containing the angle between the three atoms.

        Raises
        ------
        TypeError
            This occurs when one of the atom labels in the input angle tuple
            does not have corresponding data in final_geom.
        """
        final_geom = \
            FinalGeometry(out_filename=self._out_filename,
                          outfile_contents=self._outfile_contents,
                          inputs=(
                                angle_tuple[0],
                                angle_tuple[1],
                                angle_tuple[2]
                            ))

        atom0, atom1, atom2 = angle_tuple[0], angle_tuple[1], angle_tuple[2]
        # I've decided DRY here is more trouble than its worth...
        try:
            atom0_x = float(final_geom.get_datum(atom0)['x'])
            atom0_y = float(final_geom.get_datum(atom0)['y'])
            atom0_z = float(final_geom.get_datum(atom0)['z'])
        except TypeError:
            print(f'Manual calculation failed for bond angle {atom0}-{atom1}-'
                  f'{atom2}: geometry data for {atom0} not found.')
            return None
        try:
            atom1_x = float(final_geom.get_datum(atom1)['x'])
            atom1_y = float(final_geom.get_datum(atom1)['y'])
            atom1_z = float(final_geom.get_datum(atom1)['z'])
        except TypeError:
            print(f'Manual calculation failed for bond angle {atom0}-{atom1}-'
                  f'{atom2}: geometry data for {atom1} not found.')
            return None
        try:
            atom2_x = float(final_geom.get_datum(atom2)['x'])
            atom2_y = float(final_geom.get_datum(atom2)['y'])
            atom2_z = float(final_geom.get_datum(atom2)['z'])
        except TypeError:
            print(f'Manual calculation failed for bond angle {atom0}-{atom1}-'
                  f'{atom2}: geometry data for {atom2} not found.')
            return None
        vector_01 = [atom0_x - atom1_x, atom0_y - atom1_y, atom0_z - atom1_z]
        vector_12 = [atom1_x - atom2_x, atom1_y - atom2_y, atom1_z - atom2_z]
        numerator = (vector_01[0] * vector_12[0]) + \
                    (vector_01[1] * vector_12[1]) + \
                    (vector_01[2] * vector_12[2])
        denominator = math.sqrt(vector_01[0] ** 2 +
                                vector_01[1] ** 2 +
                                vector_01[2] ** 2) * \
                      math.sqrt(vector_12[0] ** 2 +
                                vector_12[1] ** 2 +
                                vector_12[2] ** 2)
        return str(
            round(180 - math.degrees(math.acos(numerator / denominator)), 5)
        )

    def get_datum(self, angle_tuple):
        """
        Gives the bond angle from _data for a certain bond.

        Parameters
        ----------
        angle_tuple : tuple
            Tuple containing three atom labels, representing the desired bond.

        Returns
        -------
        str
            String consisting of the angle of the corresponding bond in degrees.

        Raises
        ------
        KeyError
            This occurs when the input 'bond' tuple can't be found as a key in
            the dict containing the bond angle data.
        """
        # In order to find the bond angle no matter which atom is listed first
        # in the bond tuple, this override is necessary.
        try:
            return self._data[angle_tuple]
        except KeyError:
            try:
                flipped_angle_tuple = (angle_tuple[2],
                                       angle_tuple[1],
                                       angle_tuple[0])
                return self._data[flipped_angle_tuple]
                pass
            except KeyError:
                print(f'Error: {angle_tuple} not found in '
                      f'{self._out_filename} (Bond Angles).')
                return None
