#!/usr/bin/env python3
"""
Provides a Builder which creates StructureData instances.

This class uses the Builder design pattern to create instances of
the StructureData class based on a given filename for an input .txt file.
"""
__author__ = "Peter Waddell"
__copyright__ = "Copyright 2024"
__credits__ = ["Peter Waddell"]
__version__ = "0.1.0"
__date__ = "2024/02/27"
__maintainer__ = "Peter Waddell"
__email__ = "pmwaddell9@gmail.com"
__status__ = "Prototype"

from structure_data import StructureData
from input_reader import InputReader
from initial_geom import InitialGeometry
from final_geom import FinalGeometry
from mulliken_charges import MullikenCharges
from mulliken_charge_sums import MullikenChargeSums
from loewdin_charges import LoewdinCharges
from loewdin_charge_sums import LoewdinChargeSums
from homo_lumo_energies import HOMOLUMOEnergies
from bond_lengths import BondLengths
from bond_angles import BondAngles
from polarizability import Polarizability
from dipole_moments import DipoleMoments


class StructureDataBuilder:
    """
    A Builder which creates StructureData instances.

    Attributes
    ----------
    __input_filename : str
        String of filename of .txt file that contains lists of desired atom
        labels for each type of data that will be pulled from the .out file.
    __input_reader : InputReader
        Instance of InputReader used to retrieve the inputs for the
        StructureData objects this instance builds.
    """
    def __init__(self, input_filename):
        """
        Parameters
        ----------
        input_filename : str
            String of filename of .txt file that contains lists of desired atom
            labels for each type of data that will be pulled from the .out file.
        """
        self.__input_filename = input_filename
        # TODO: another opportunity for Dependency Injection???? or not????
        self.__input_reader = InputReader(input_filename)

    def build(self, out_filename):
        """
        Creates and returns an instance of StructureData based on the passed
        .out filename and the input filename attribute.

        Parameters
        ----------
        out_filename : str
            String of filename of desired .out file.

        Returns
        -------
        StructureData
            Instance of StructureData based on the passed .out filename and the
            input filename attribute.
        """

        def create_data_sections():
            """
            Creates a dictionary to be passed to the StructureData constructor;
            this dict is held as the __data_sections attribute of that object.

            Returns
            -------
            dict
                Dictionary mapping strings of section names to corresponding
                DataSection subclasses related to the Schrödinger .out file,
                which are instantiated based on inputs from __input_reader.
            """
            def add_inputs_section(name, data_section, inputs=()):
                """
                Adds a key-value pair to data_sections: the key is the name of
                the particular DataSection subclass to be added, and the value
                is the instance of this subclass.

                Parameters
                ----------
                name : str
                    Name of the DataSection subclass.
                data_section : DataSection
                    Instance of the DataSection subclass.
                inputs : tuple
                    Tuple of inputs from __input_reader for the particular
                    DataSection subclass.
                """
                if inputs:
                    data_sections[name] = \
                        data_section(out_filename=out_filename,
                                     outfile_contents=outfile_contents,
                                     inputs=inputs)

            data_sections = {}
            # TODO: possibly abstract this to make this class plug-n-play
            add_inputs_section('Initial Geometry', InitialGeometry,
                               self.__input_reader.get_initial_geom_inputs())
            add_inputs_section('Final Geometry', FinalGeometry,
                               self.__input_reader.get_final_geom_inputs())
            add_inputs_section('Bond Lengths', BondLengths,
                               self.__input_reader.get_bond_length_inputs())
            add_inputs_section('Bond Angles', BondAngles,
                               self.__input_reader.get_bond_angle_inputs())
            data_sections['Polarizability'] = \
                Polarizability(out_filename=out_filename,
                               outfile_contents=outfile_contents)
            data_sections['Dipole Moments'] = \
                DipoleMoments(out_filename=out_filename,
                              outfile_contents=outfile_contents)
            data_sections['HOMO LUMO Energies'] = \
                HOMOLUMOEnergies(out_filename=out_filename,
                                 outfile_contents=outfile_contents)
            add_inputs_section('Mulliken Charges', MullikenCharges,
                               self.__input_reader.get_mulliken_charge_inputs())
            add_inputs_section('Mulliken Charge Sums', MullikenChargeSums,
                               self.__input_reader.
                               get_mulliken_charge_sum_inputs())
            add_inputs_section('Loewdin Charges', LoewdinCharges,
                               self.__input_reader.get_loewdin_charge_inputs())
            add_inputs_section('Loewdin Charge Sums', LoewdinChargeSums,
                               self.__input_reader.
                               get_loewdin_charge_sum_inputs())
            return data_sections

        outfile_contents = self.__read_file(out_filename)
        return StructureData(
            out_filename, self.__input_filename, create_data_sections())

    # TODO: probs will make this another class I guess for reading files I mean
    @staticmethod
    def __read_file(f):
        """
        Converts a text file to a single string using .read().

        Parameters
        ----------
        f : str
            Filename of the desired file to read.

        Returns
        -------
        contents : str
            String containing the full text of the file.

        Raises
        ------
        FileNotFoundError
            If f is not the filename of a file in the current directory.
        """
        try:
            with open(f) as file_object:
                contents = file_object.read()
        except FileNotFoundError:
            print(f"File {f} not found")
        else:
            file_object.close()
            return contents
