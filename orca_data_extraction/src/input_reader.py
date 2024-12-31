#!/usr/bin/env python3
"""
Structures subclasses that represent "Input Readers".

For our purposes, "Input Readers" read in information from the user related to
what data they want to extract from the ORCA .out file.
"""
__author__ = "Peter Waddell"
__copyright__ = "Copyright 2024"
__credits__ = ["Peter Waddell"]
__version__ = "0.1.0"
__date__ = "2024/12/30"
__maintainer__ = "Peter Waddell"
__email__ = "pmwaddell9@gmail.com"
__status__ = "Prototype"

from abc import ABC, abstractmethod


class InputReader(ABC):
    """
    Finds and stores input data for DataSection subclasses from an input file.
    """
    def __init__(self, input_filename):
        self._input_filename = input_filename

    @abstractmethod
    def get_initial_geom_inputs(self):
        """Returns initial geometry inputs."""
        pass

    @abstractmethod
    def get_final_geom_inputs(self):
        """Returns final geometry inputs."""
        pass

    @abstractmethod
    def get_bond_length_inputs(self):
        """Returns  of bond length inputs."""
        pass

    @abstractmethod
    def get_bond_angle_inputs(self):
        """Returns bond angle inputs."""
        pass

    @abstractmethod
    def get_mulliken_charge_inputs(self):
        """Returns Mulliken charge inputs."""
        pass

    @abstractmethod
    def get_mulliken_charge_sum_inputs(self):
        """Returns Mulliken charge sum inputs."""
        pass

    @abstractmethod
    def get_loewdin_charge_inputs(self):
        """Returns Loewdin charge inputs."""
        pass

    @abstractmethod
    def get_loewdin_charge_sum_inputs(self):
        """Returns Loewdin charge sum inputs."""
        pass
