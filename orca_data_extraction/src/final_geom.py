#!/usr/bin/env python3
"""
The FinalGeometry class searches for and stores the final structure geometry
data (i.e., after geometry optimization is complete) from an ORCA .out file.
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


class FinalGeometry(DataSectionWithInputs):
    """
    Finds and stores the final geometry data from an ORCA .out file.

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
            Tuple of atom labels (e.g. '2 H') for which final geometry data
            will be searched.
        """
        super().__init__(out_filename, outfile_contents, inputs)
        self._section_name = 'Final Geometry'

    def _search(self, atom_label):
        """
        Use regex to search .out file for an atom's final geom. coordinates.

        Parameters
        ----------
        atom_label : str
            String of the desired atom label.

        Returns
        -------
        dict
            A dictionary containing 'x', 'y' and 'z' as keys and the
            corresponding final geometry coordinates (in Å) for the atom label
            as values (as strings).

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

        def __reverse_string_by_lines(s):
            """
            Reverses a string in terms of the order of its lines.

            Parameters
            ----------
            s: str
                String to be reversed line-by-line

            Returns
            -------
            str
                Reversed string, line-by-line.
            """
            s = s.splitlines()[::-1]
            return '\n'.join(s)

        re_atom_label = __convert_str_for_verbose_regex(atom_label)

        # Here I am assuming that the last occurrence of geometry data in the
        # .out file will represent the finished calculation, seems logical...

        # However, I found that in order to find the last occurrence without
        # catastrophic backtracking, it was necessary to reverse the line order
        # of the outfile contents string, then match the first occurrence there.
        reversed_contents = \
            __reverse_string_by_lines(self._outfile_contents)

        # Note that, consequently, this regex string is INVERTED to match!!!
        # Note also: \ must be used for all whitespace I want to count
        # when using verbose regular expressions.
        regex_geom_opt = re.compile(
            fr"""
            (INTERNAL\ COORDINATES\ \(ANGSTROEM\))
            (.*?)               # all text until data begins
            ((\ |\n){re_atom_label})
            # above: (\ |\n) prevents '1 H' from matching e.g. '11 H' when '1 H' is not present
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
            (CARTESIAN\ COORDINATES\ \(A.U.\))
            # above: prevents accidental matches later in the .out file
            """,
            flags=re.VERBOSE | re.DOTALL
        )
        try:
            result = regex_geom_opt.search(reversed_contents)
            x = __convert_au_to_angstrom(result.group(12))
            y = __convert_au_to_angstrom(result.group(14))
            z = __convert_au_to_angstrom(result.group(16))
            return {'x': str(x), 'y': str(y), 'z': str(z)}
        except AttributeError:
            print(f'Error: {atom_label} was not found'
                  f' in {self._out_filename} (Final Geometry).')
            return {'x': None,
                    'y': None,
                    'z': None}
