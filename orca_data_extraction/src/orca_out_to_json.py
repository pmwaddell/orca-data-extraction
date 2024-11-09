#!/usr/bin/env python3
"""
A script to quickly pull desired data from an ORCA .out file and compile
it into a JSON file.

Before running, the user should specify what information they want to look for
in a .txt file (see example). When executed, the script checks each file in the
working directory. If the file ends in .out, it exports the desired data into
a JSON file.
"""
__author__ = "Peter Waddell"
__copyright__ = "Copyright 2024"
__credits__ = ["Peter Waddell"]
__version__ = "0.1.0"
__date__ = "2024/03/01"
__maintainer__ = "Peter Waddell"
__email__ = "pmwaddell9@gmail.com"
__status__ = "Prototype"

import os
import json
import sys

from orca_data_extraction.src.structure_data_builder import StructureDataBuilder


def make_json_list(sd_list):
    """
    Converts the data in a list of StructureData instances to a dict for JSON.

    Parameters
    ----------
    sd_list : list
        List containing the set of StructureData instances that each come
        from the ORCA .out files.

    Returns
    -------
    list
        List with the data from sd_list configured to be compatible with
        JSON (i.e., tuples are converted to strings).
    """
    def format_column_name(x):
        """
        Format string for use as a column name in the JSON file.

        Parameters
        ----------
        x : str or other
            Entity to be potentially renamed.

        Returns
        -------
        str or other
            A string formatted for use as column name in the JSON file, or returns
            the object unchanged if it is not a string (e.g., a dict).
        """
        if type(x) != str:
            return x
        else:
            return x\
                .replace("'", "")\
                .replace(', ', ',')\
                .replace(' ', '_')\
                .lower()

    json_lst = []
    for sd in sd_list:
        sd_data = {
            'script_input_filename': sd.get_input_filename(),
            'orca_out_filename': sd.get_out_filename()
        }
        for data_section in sd.get_data_sections().values():
            data_section_data = data_section.get_data()
            json_safe_data = {}
            # JSON is not compatible with tuples, so must convert to str
            for key in data_section_data.keys():
                val = data_section_data[key]
                key_to_add, val_to_add = key, val
                if type(val) == tuple:
                    val_to_add = str(val)
                if type(key) == tuple:
                    key_to_add = str(key)
                json_safe_data[format_column_name(key_to_add)] = \
                    format_column_name(val_to_add)
            sd_data[
                data_section.get_section_name().replace(' ', '_').lower()
            ] = json_safe_data
        json_lst.append(sd_data)
    return json_lst


def create_json_from_sds(sd_list, json_name):
    """
    Writes the data in a list of StructureData instances to a JSON file.

    Parameters
    ----------
    sd_list : list
        List containing the set of StructureData instances that each come
        from the ORCA .out files.
    json_name : str
        Name of the JSON file where the data will be stored.
    """
    json_list = make_json_list(sd_list)
    with open(f'{json_name}.json', 'w') as f:
        json.dump(json_list, f, indent=2)


def main():
    # TODO: use an argument parser here instead? make argument inputs more sophisticated?
    json_name = ''
    # Process command line arguments
    # TODO: extract this part for each file type?? let the user select the file type @ command line?
    if len(sys.argv) >= 2:
        inputs_name = sys.argv[1]
        if not os.path.isfile(inputs_name):
            print('No file with name ' + inputs_name + ' found.')
            quit()
        if len(sys.argv) >= 3:
            json_name = sys.argv[2]
    else:
        print('Script will execute on all .out files in the current '
              'working directory.')
        while True:
            print('Name of input file with atom labels ("q" to quit): ',
                  end='')
            inputs_name = input()
            if inputs_name == 'q':
                quit()
            if not os.path.isfile(os.getcwd() + "\\" + inputs_name):
                print('No file with name ' + inputs_name + ' found.')
                continue
            break

    # Ask for excel file name
    if json_name == '':
        print('Name of the JSON file which will contain the data (press ENTER '
              'to use the default name, "q" to quit): ', end='')
        json_name = input()
        if json_name == 'q':
            quit()
        # If the user just hits enter, use default name:
        if json_name == '':
            json_name = f'ORCA_data_{inputs_name[:-4]}'

    print('')
    sd_list = []
    structure_data_builder = StructureDataBuilder(inputs_name)
    for f in os.listdir(os.getcwd()):
        if os.path.isfile(f):
            try:
                filename_end = f[-4:]
            except IndexError:
                # Since it is hard for filenames to be shorter than 4 chars
                # I think it is unlikely this error would ever be raised...
                print(f'{f}: Invalid filename')
                continue
            if filename_end == '.out':
                try:
                    print(f'Beginning search: {f}')
                    sd_list.append(structure_data_builder.build(f))
                    print(f'{f} complete.\n')
                except IndexError:
                    print(f'Something went wrong with {f} and it threw '
                          f'an IndexError...\n')

    create_json_from_sds(sd_list, json_name)
    print(f'Process complete! Results saved as "{json_name}.json"')


if __name__ == '__main__':
    main()
