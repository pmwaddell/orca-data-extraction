#!/usr/bin/env python3
"""
The Polarizability class searches for and stores polarizability data from
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
from data_section import DataSection


class Polarizability(DataSection):
    """
    Finds and stores polarizability data from a ORCA .out file.

    Attributes
    ----------
    __regex : str
        Regular expression string used to search the .out file for the
        polarizability data.

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
        self.__regex = re.compile(
            r"""
            (THE\ POLARIZABILITY\ TENSOR)
            (.*?)               # all text until data begins
            (The\ raw\ cartesian\ tensor\ \(atomic\ units\):)
            (\n\ *)             # newline plus whitespace
            (-?[\d]+[.][\d]+)   # alpha (x x) tensor component
            (\ *)               # whitespace
            (-?[\d]+[.][\d]+)   # alpha (x y) tensor component
            (\ *)
            (-?[\d]+[.][\d]+)   # alpha (x z) tensor component
            (\ *\n\ *)          # whitespace on either end of a newline
            (-?[\d]+[.][\d]+)   # alpha (y x) tensor component
            (\ *)
            (-?[\d]+[.][\d]+)   # alpha (y y) tensor component
            (\ *)
            (-?[\d]+[.][\d]+)   # alpha (y z) tensor component
            (\ *\n\ *)
            (-?[\d]+[.][\d]+)   # alpha (z x) tensor component
            (\ *)
            (-?[\d]+[.][\d]+)   # alpha (z y) tensor component
            (\ *)
            (-?[\d]+[.][\d]+)   # alpha (z z) tensor component
            (.*?)
            (Isotropic\ polarizability\ :)
            (\ *)
            (-?[\d]+[.][\d]+)   # isotropic polarizability
            (.*?)
            (Timings\ for\ individual\ modules:)
            # above: prevents accidental matches later in the .out file
            """,
            flags=re.VERBOSE | re.DOTALL
        )
        super().__init__(out_filename, outfile_contents)
        self._section_name = 'Polarizability'

    def _find_data(self):
        """
        Search the .out file for polarizability data, return as dict.

        Returns
        -------
        dict
            Dictionary containing polarizability parameters as keys and the
            corresponding polarizability values (in AU) as values (as strings).

        Raises
        ------
        AttributeError
            This occurs when the regex fails to find what it is looking
            for, and returns NoneType. Then, .group(n) gives this error.
        """
        try:
            result = self.__regex.search(self._outfile_contents)
            alpha_xx = result.group(5)
            alpha_xy = result.group(7)
            alpha_xz = result.group(9)
            alpha_yx = result.group(11)
            alpha_yy = result.group(13)
            alpha_yz = result.group(15)
            alpha_zx = result.group(17)
            alpha_zy = result.group(19)
            alpha_zz = result.group(21)
            alpha = result.group(25)
            return {'alpha_xx': alpha_xx, 'alpha_xy': alpha_xy,
                    'alpha_xz': alpha_xz, 'alpha_yx': alpha_yx,
                    'alpha_yy': alpha_yy, 'alpha_yz': alpha_yz,
                    'alpha_zx': alpha_zx, 'alpha_zy': alpha_zy,
                    'alpha_zz': alpha_zz, 'alpha': alpha}
        except AttributeError:
            print(f'Polarizability data not found in {self._out_filename}.')
            error_msg = 'ERROR: polarizability data not found'
            # TODO: consider using NULL instead of an error message string?
            # consider that this may cause problems when putting the data into excel? test it first, then do the replacement
            return {'alpha_xx': error_msg, 'alpha_xy': error_msg,
                    'alpha_xz': error_msg, 'alpha_yx': error_msg,
                    'alpha_yy': error_msg, 'alpha_yz': error_msg,
                    'alpha_zx': error_msg, 'alpha_zy': error_msg,
                    'alpha_zz': error_msg, 'alpha': error_msg}
