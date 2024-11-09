#!/usr/bin/env python3
"""
The HOMOLUMOEnergies class searches for and stores the HOMO and LUMO energy
data from an ORCA .out file.
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

from orca_data_extraction.src.data_section import DataSection


class HOMOLUMOEnergies(DataSection):
    """
    Finds and stores HOMO and LUMO energy data from a ORCA .out file.

    Attributes
    ----------
    __regex : str
        Regular expression string used to search the .out file for the
        HOMO and LUMO energy data.

    Methods
    -------
    _find_data
        Search the .out file for HOMO and LUMO energy data, return as dict.
    """
    def __init__(self, out_filename, outfile_contents):
        """
        Parameters
        ----------
        out_filename : str
            Name of the ORCA .out file that will be searched.
        outfile_contents : str
            String containing the full text of the ORCA .out file.
        """
        # Here I am assuming that the last occurrence of the MO energy data in
        # the .out file will be from the finished calculation, seems logical...

        # However, I found that in order to find the last occurrence without
        # catastrophic backtracking, it was necessary to reverse the line order
        # of the outfile contents string, then match the first occurrence there.

        # Note that, consequently, this regex string is INVERTED to match!!!
        # Note also: \ must be used for all whitespace I want to count
        # when using verbose regular expressions.
        self.__regex = re.compile(
            r"""
            (MULLIKEN\ POPULATION\ ANALYSIS)
            (.*?)               # all text until data begins
            (0.0000)            # LUMO occupancy, always 0 of course
            (\ *)               # whitespace
            (-?[\d]+[.][\d]+)   # LUMO energy in Eh
            (\ *)
            (-?[\d]+[.][\d]+)   # LUMO energy in eV
            (\ \n)              # newline
            (\ *)  
            ([\d]+)             # HOMO orbital number
            (\ \ \ )
            (1|2)               # HOMO occupancy
            (.0000)
            (\ *)
            (-?[\d]+[.][\d]+)   # HOMO energy in Eh
            (\ *)
            (-?[\d]+[.][\d]+)   # HOMO energy in eV
            (.*?)
            (ORBITAL\ ENERGIES)
            # above: prevents accidental matches later in the .out file
            """,
            flags=re.VERBOSE | re.DOTALL
        )
        super().__init__(out_filename, outfile_contents)
        self._section_name = 'HOMO LUMO Energies'

    def _find_data(self):
        """
        Search the .out file for HOMO and LUMO energy data, return as dict.

        Returns
        -------
        dict
            Dictionary containing HOMO/LUMO energy as keys and the
            corresponding energy values (in eV) as values (as strings).

        Raises
        ------
        AttributeError
            This occurs when the regex fails to find what it is looking
            for, and returns NoneType. Then, .group(n) gives this error.
        """
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
        # See above comments: in order to match the LAST occurrence of the MO
        # energy data in the .out file, the contents must be reversed.
        reversed_contents = \
            __reverse_string_by_lines(self._outfile_contents)
        try:
            result = self.__regex.search(reversed_contents)
            homo_energy = result.group(17)
            lumo_energy = result.group(7)
            return {'HOMO energy': homo_energy, 'LUMO energy': lumo_energy}
        except AttributeError:
            print(f'HOMO/LUMO energy data not found in '
                  f'{self._out_filename}')
            return {'HOMO energy': None, 'LUMO energy': None}

