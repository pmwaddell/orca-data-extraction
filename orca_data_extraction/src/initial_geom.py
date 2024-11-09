#!/usr/bin/env python3
"""
The FinalGeometry class searches for and stores the initial (i.e., input by the
user) geometry data from an ORCA .out file.
"""
__author__ = "Peter Waddell"
__copyright__ = "Copyright 2024"
__credits__ = ["Peter Waddell"]
__version__ = "0.1.0"
__date__ = "2024/02/26"
__maintainer__ = "Peter Waddell"
__email__ = "pmwaddell9@gmail.com"
__status__ = "Prototype"

import re

from orca_data_extraction.src.data_section_with_inputs import DataSectionWithInputs


class InitialGeometry(DataSectionWithInputs):
    """
    Finds and stores initial geometry data from an ORCA .out file.

    Methods
    -------
    _search
        Search the .out file for bond length data.
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
            Tuple of atom labels (e.g. '2 H') for which input geometry data
            will be searched.
        """
        super().__init__(out_filename, outfile_contents, inputs)
        self._section_name = 'Initial Geometry'

    def _search(self, atom_label):
        """
        Use regex to search .out file for an atom's initial geom. coordinates.

        Meaning, the coordinates that the user input for the calculation. In
        the case of single point calculations, these coordinates will be the
        same as the final coordinates, but for geometry optimizations they
        should be different.

        Parameters
        ----------
        atom_label : str
            String of the desired atom label.

        Returns
        -------
        dict
            A dictionary containing 'x', 'y' and 'z' as keys and the
            corresponding initial geometry coordinates (in Å) for the atom
            label as values (as strings).

        Raises
        ------
        AttributeError
            This occurs when the regex fails to find what it is looking
            for, and returns NoneType. Then, .group(n) gives this error.
        """
        def __convert_str_for_verbose_regex(s):
            """
            Converts string to a form that works properly for verbose REs.

            Verbose regular expressions ignore whitespace, unless preceded by a
            "\" (backslash) character. To use such a string as part of a
            verbose RE, this character must be added before each space first;
            this function returns a version of the input string modified
            in this way.

            Parameters
            ----------
            s: str
                Input string.

            Returns
            -------
            result: str
                A modified version of the input string which now has "\"
                preceding each whitespace character.
            """
            result = ''
            for i in range(len(s)):
                if s[i] == ' ':
                    result = result + r'\ '
                else:
                    result = result + s[i]
            return result

        def __convert_au_to_angstrom(x):
            """
            Converts a value from AU to Ångstroms.

            Parameters
            ----------
            x
                Value in AU to be converted.

            Returns
            -------
            float
                Value of x in Ångstroms.
            """
            x = float(x)
            return round(x * 0.529177, 5)

        re_atom_label = __convert_str_for_verbose_regex(atom_label)
        # Here I am assuming that the first occurrence of geometry data in the
        # .out file will represent the coordinates which were input by the
        # user, for either geometry optimizations or single point calculations.
        regex_geom_opt = re.compile(
            fr"""
            (CARTESIAN\ COORDINATES\ \(A.U.\))
            (.*?)               # all text until data begins
            ((\ |\n){re_atom_label})
            (\ *)               # whitespace
            (-?[\d]+[.][\d]+)   # ZA, unwanted information here
            (\ *)
            ([\d]+)             # FRAG, unwanted information here
            (\ *)
            (-?[\d]+[.][\d]+)   # MASS, unwanted information here
            (\ *)
            (-?[\d]+[.][\d]+)   # X coordinate
            (\ *)
            (-?[\d]+[.][\d]+)   # Y coordinate
            (\ *)
            (-?[\d]+[.][\d]+)   # Z coordinate
            (.*?)
            (INTERNAL\ COORDINATES)
            # above: prevents accidental matches later in the .out file
            """,
            flags=re.VERBOSE | re.DOTALL
        )
        try:
            result = regex_geom_opt.search(self._outfile_contents)
            x = __convert_au_to_angstrom(result.group(12))
            y = __convert_au_to_angstrom(result.group(14))
            z = __convert_au_to_angstrom(result.group(16))
            return {'x': str(x), 'y': str(y), 'z': str(z)}
        except AttributeError:
            print(f'Error: {atom_label} was not found'
                  f' in {self._out_filename} (Initial Geometry).')
            return {'x': None,
                    'y': None,
                    'z': None}
