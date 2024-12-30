#!/usr/bin/env python3
__author__ = "Peter Waddell"
__copyright__ = "Copyright 2024"
__credits__ = ["Peter Waddell"]
__version__ = "0.1.1"
__date__ = "2024/12/30"
__maintainer__ = "Peter Waddell"
__email__ = "pmwaddell9@gmail.com"
__status__ = "Prototype"

import unittest
import math
from orca_data_extraction.src.structure_data_builder import StructureDataBuilder


class TestStructureData(unittest.TestCase):
    """Tests for the class StructureData"""

    def setUp(self):
        """
        Create test instances of StructureData for use in all test methods.

        Both are based on triphenylphosphine (PPh3): one is for a geometry
        optimization (PPh3_opt.out), the other a single point calculation
        (PPh3_sp.out); finally, another variant skips the Bond Lengths section.
        """
        sd_builder = StructureDataBuilder('PPh3_test_input.json')
        self.test_sd_opt = sd_builder.build('PPh3_opt.out')
        self.test_sd_sp = sd_builder.build('PPh3_sp.out')
        sd_builder_skip = StructureDataBuilder('PPh3_test_input_skip.json')
        self.test_sd_skip = sd_builder_skip.build('PPh3_opt.out')

    def test_skip_section(self):
        """
        Tests that the proper message is returned when attempting to access
        data in a data section that has been skipped/is not present.
        """
        self.assertEqual(self.test_sd_skip.get_data_section('Bond Lengths'),
                         'ERROR: Data section Bond Lengths not found in '
                         'PPh3_test_input_skip.json (input file).')
        self.assertEqual(self.test_sd_skip.get_data_section_datum(
            'Bond Lengths', ()),
            'ERROR: Data section Bond Lengths not found in PPh3_test_input_skip.json '
            '(input file).')
        print('Section skipping test complete.\n')

    def test_find_initial_geom_data(self):
        """
        Tests that the initial geometry data is found correctly.
        """
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Initial Geometry', '0 P')['x']),
                -1.89823,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Initial Geometry', '0 P')['y']),
                2.49748,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Initial Geometry', '0 P')['z']),
                0.0,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_sp.get_data_section_datum(
                    'Initial Geometry', '0 P')['x']),
                -1.97759,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_sp.get_data_section_datum(
                    'Initial Geometry', '0 P')['y']),
                2.94534,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_sp.get_data_section_datum(
                    'Initial Geometry', '0 P')['z']),
                0.09181,
                rel_tol=0.0001)
        )
        # Test that '1 H' does not match '11 H' accidentally
        self.assertEqual(
            self.test_sd_opt.get_data_section_datum(
                'Initial Geometry', '1 H')['x'],
            None
        )
        self.assertEqual(
            self.test_sd_opt.get_data_section_datum(
                'Initial Geometry', '11 B')['x'],
            None
        )
        print('Initial geometry test complete.\n')

    def test_find_final_geom_data(self):
        """
        Tests that the final geometry data is found correctly.
        """
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Final Geometry', '0 P')['x']),
                -1.97759,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Final Geometry', '0 P')['y']),
                2.94534,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Final Geometry', '0 P')['z']),
                0.09181,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_sp.get_data_section_datum(
                    'Final Geometry', '0 P')['x']),
                -1.97759,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_sp.get_data_section_datum(
                    'Final Geometry', '0 P')['y']),
                2.94534,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_sp.get_data_section_datum(
                    'Final Geometry', '0 P')['z']),
                0.09181,
                rel_tol=0.0001)
        )
        # Test that '1 H' does not match '11 H' accidentally
        self.assertEqual(
            self.test_sd_opt.get_data_section_datum(
                'Final Geometry', '1 H')['x'],
            None
        )
        self.assertEqual(
            self.test_sd_opt.get_data_section_datum(
                'Final Geometry', '11 B')['x'],
            None
        )
        print('Final geometry test complete.\n')

    def test_find_bond_length_datum(self):
        """
        Tests that the bond length data is found correctly.
        """
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Bond Lengths', ('0 P', '1 C'))),
                1.85902,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Bond Lengths', ('1 C', '0 P'))),
                1.85902,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Bond Lengths', ('19 C', '20 H'))),
                1.10156,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_sp.get_data_section_datum(
                    'Bond Lengths', ('1 C', '2 C'))),
                1.41487,
                rel_tol=0.0001)
        )
        # Should be possible to ask for data using either order of atom labels
        self.assertTrue(
            math.isclose(
                float(self.test_sd_sp.get_data_section_datum(
                    'Bond Lengths', ('2 C', '1 C'))),
                1.41487,
                rel_tol=0.0001)
        )
        # These atoms are not actually bonded
        self.assertTrue(
            math.isclose(
                float(self.test_sd_sp.get_data_section_datum(
                    'Bond Lengths', ('0 P', '20 H'))),
                5.07423,
                rel_tol=0.0001)
        )
        self.assertEqual(
            self.test_sd_opt.get_data_section_datum(
                'Bond Lengths', ('19 C', '11 B')),
            None
        )
        self.assertEqual(
            self.test_sd_opt.get_data_section_datum(
                'Bond Lengths', ('19 C', '43 N')),
            None
        )
        print('Bond length test complete.\n')

    def test_find_bond_angle_datum(self):
        """
        Tests that the bond angle data is found correctly.
        """
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Bond Angles', ('0 P', '1 C', '2 C'))),
                116.78352,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Bond Angles', ('1 C', '2 C', '3 H'))),
                119.50915,
                rel_tol=0.0001)
        )
        # Should be possible to ask for data using either order of atom labels
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Bond Angles', ('3 H', '2 C', '1 C'))),
                119.50915,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_sp.get_data_section_datum(
                    'Bond Angles', ('0 P', '1 C', '2 C'))),
                116.78352,
                rel_tol=0.0001)
        )
        # Arbitrary three atoms
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Bond Angles', ('0 P', '3 H', '18 H'))),
                59.45174,
                rel_tol=0.0001)
        )
        self.assertEqual(
            self.test_sd_opt.get_data_section_datum(
                'Bond Angles', ('1 S', '2 S', '3 S')),
            None
        )
        print('Bond angle test complete.\n')

    def test_find_polarizability_datum(self):
        """
        Tests that the polarizability data is found correctly.
        """
        self.assertTrue(
            math.isclose(
                float(self.test_sd_sp.get_data_section_datum(
                    'Polarizability', 'alpha_xx')),
                236.30256,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_sp.get_data_section_datum(
                    'Polarizability', 'alpha')),
                216.30179,
                rel_tol=0.0001)
        )
        self.assertEqual(
            self.test_sd_opt.get_data_section_datum(
                'Polarizability', 'alpha_xx'),
            None
        )
        print('Polarizability test complete.\n')

    def test_find_dipole_moments_datum(self):
        """
        Tests that the dipole moment data is found correctly.
        """
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Dipole Moments', 'X')),
                0.11095,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Dipole Moments', 'Tot')),
                0.50493,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_sp.get_data_section_datum(
                    'Dipole Moments', 'Y')),
                -0.43806,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_sp.get_data_section_datum(
                    'Dipole Moments', 'Tot')),
                0.49464,
                rel_tol=0.0001)
        )
        print('Dipole moment test complete.\n')

    def test_homo_lumo_datum(self):
        """
        Tests that the dipole moment data is found correctly.
        """
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'HOMO LUMO Energies', 'HOMO energy')),
                -5.2494,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'HOMO LUMO Energies', 'LUMO energy')),
                -1.6248,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_sp.get_data_section_datum(
                    'HOMO LUMO Energies', 'HOMO energy')),
                -5.8242,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_sp.get_data_section_datum(
                    'HOMO LUMO Energies', 'LUMO energy')),
                -0.7180,
                rel_tol=0.0001)
        )
        print('HOMO LUMO energy test complete.\n')

    def test_find_mulliken_charge_datum(self):
        """
        Tests that the Mulliken charge data is found correctly.
        """
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Mulliken Charges', '0 P')),
                0.303926,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_sp.get_data_section_datum(
                    'Mulliken Charges', '19 C')),
                0.019255,
                rel_tol=0.0001)
        )
        # Test that '1 H' does not match '11 H' accidentally
        self.assertEqual(
            self.test_sd_opt.get_data_section_datum('Mulliken Charges', '1 H'),
            None
        )
        self.assertEqual(
            self.test_sd_opt.get_data_section_datum('Mulliken Charges', '11 B'),
            None
        )
        self.assertEqual(
            self.test_sd_opt.get_data_section_datum('Mulliken Charges', '5 S'),
            None
        )
        print('Mulliken charge test complete.\n')

    def test_find_mulliken_charge_sum_datum(self):
        """
        Tests that the Mulliken charge sum data is found correctly.
        """
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Mulliken Charge Sums',
                    ('0 P', '1 C', '18 H', '19 C', '2 C', '3 H'))),
                0.175208,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Mulliken Charge Sums', ('0 P', '3 H'))),
                0.309018,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Mulliken Charge Sums', ('3 H', '0 P'))),
                0.309018,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Mulliken Charge Sums', ('0 P',))),
                0.303926,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_sp.get_data_section_datum(
                    'Mulliken Charge Sums',
                    ('0 P', '1 C', '18 H', '19 C', '2 C', '3 H'))),
                0.217798,
                rel_tol=0.0001)
        )
        self.assertEqual(
            self.test_sd_opt.get_data_section_datum(
                'Mulliken Charge Sums',
                ('0 P', '1 C', '11 B', '19 C', '2 C', '3 H')),
            None
        )
        print('Mulliken charge sum test complete.\n')

    def test_find_loewdin_charge_datum(self):
        """
        Tests that the Loewdin charge data is found correctly.
        """
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Loewdin Charges', '0 P')),
                0.501961,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_sp.get_data_section_datum(
                    'Loewdin Charges', '19 C')),
                -0.027309,
                rel_tol=0.0001)
        )
        # Test that '1 H' does not match '11 H' accidentally
        self.assertEqual(
            self.test_sd_opt.get_data_section_datum('Loewdin Charges', '1 H'),
            None
        )
        self.assertEqual(
            self.test_sd_opt.get_data_section_datum('Loewdin Charges', '11 B'),
            None
        )
        self.assertEqual(
            self.test_sd_opt.get_data_section_datum('Loewdin Charges', '5 S'),
            None
        )
        print('Loewdin charge test complete.\n')

    def test_find_loewdin_charge_sum_datum(self):
        """
        Tests that the Loewdin charge sum data is found correctly.
        """
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Loewdin Charge Sums',
                    ('0 P', '1 C', '18 H', '19 C', '2 C', '3 H')
                )),
                0.328838,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Loewdin Charge Sums', ('0 P', '3 H'))),
                0.533242,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Loewdin Charge Sums', ('3 H', '0 P'))),
                0.533242,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_opt.get_data_section_datum(
                    'Loewdin Charge Sums', ('0 P',))),
                0.501961,
                rel_tol=0.0001)
        )
        self.assertTrue(
            math.isclose(
                float(self.test_sd_sp.get_data_section_datum(
                    'Loewdin Charge Sums',
                    ('0 P', '1 C', '18 H', '19 C', '2 C', '3 H'))),
                0.338662,
                rel_tol=0.0001)
        )
        self.assertEqual(
            self.test_sd_opt.get_data_section_datum(
                'Loewdin Charge Sums',
                ('0 P', '1 H', '11 B', '19 C', '2 C', '3 H')),
            None
        )
        print('Loewdin charge sum test complete.\n')


if __name__ == '__main__':
    unittest.main()
