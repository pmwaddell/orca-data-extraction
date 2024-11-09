#!/usr/bin/env python3
"""
The DipoleMoments class searches for and stores dipole moment data from
an ORCA .out file.
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


class DipoleMoments(DataSection):
    """
    Finds and stores dipole moment data from a ORCA .out file.

    Attributes
    ----------
    _regex : str
        Regular expression string used to search the .out file for the
        dipole moments data.

    Methods
    -------
    _find_data
        Search the .out file for polarizability data, return as dict.
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
        # Note: \ must be used for all whitespace I want to count
        # when using verbose regular expressions.
        self._regex = re.compile(
            r"""
            (DIPOLE\ MOMENT)
            (.*?)               # all text until data begins
            (Total\ Dipole\ Moment\ \ \ \ :)
            (\ *)               # whitespace
            (-?[\d]+[.][\d]+)   # dipole moment X component
            (\ *)
            (-?[\d]+[.][\d]+)   # dipole moment Y component
            (\ *)
            (-?[\d]+[.][\d]+)   # dipole moment Z component
            (.*?)
            (Magnitude\ \(a.u.\))
            (.*?)
            (-?[\d]+[.][\d]+)   # total dipole moment
            (.*?)
            (Rotational\ spectrum)
            # above: prevents accidental matches later in the .out file
            """,
            flags=re.VERBOSE | re.DOTALL
        )
        super().__init__(out_filename, outfile_contents)
        self._section_name = 'Dipole Moments'

    def _find_data(self):
        """
        Search the .out file for dipole moment data, return as dict.

        Returns
        -------
        dict
            Dictionary containing dipole moment parameters as keys and the
            corresponding dipole moments (in AU) as values (as strings).

        Raises
        ------
        AttributeError
            This occurs when the regex fails to find what it is looking
            for, and returns NoneType. Then, .group(n) gives this error.
        """
        try:
            result = self._regex.search(self._outfile_contents)
            X = result.group(5)
            Y = result.group(7)
            Z = result.group(9)
            Tot = result.group(13)
            return {'X': X, 'Y': Y, 'Z': Z, 'Tot': Tot}
        except AttributeError:
            print(f'Dipole moments data not found in '
                  f'{self._out_filename} data.')
            return {'X': None, 'Y': None,
                    'Z': None, 'Tot': None}
