#!/usr/bin/env python3
"""
A script to quickly pull desired data from an ORCA .out file and compile
it into a CSV file.

Before running, the user should specify what information they want to look for
in a .txt file (see example). When executed, the script checks each file in the
working directory. If the file ends in .out, it exports the desired data into
a CSV file.
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
import sys
import pandas as pd

from orca_data_extraction.src.structure_data_builder import StructureDataBuilder
from orca_data_extraction.src.orca_out_to_json import make_json_list


def create_csv_from_sds(sd_list, csv_name):
    """
    Writes the data in a list of StructureData instances to a CSV file.

    Parameters
    ----------
    sd_list : list
        List containing the set of StructureData instances that each come
        from the ORCA .out files.
    csv_name : str
        Name of the CSV file where the data will be stored.
    """
    json_list = make_json_list(sd_list)
    df = pd.json_normalize(json_list)
    df.to_csv(csv_name + '.csv')


def main():
    # TODO: use an argument parser here instead? make argument inputs more sophisticated?
    csv_name = ''
    # Process command line arguments
    # TODO: extract this part for each file type?? let the user select the file type @ command line?
    if len(sys.argv) >= 2:
        inputs_name = sys.argv[1]
        if not os.path.isfile(inputs_name):
            print('No file with name ' + inputs_name + ' found.')
            quit()
        if len(sys.argv) >= 3:
            csv_name = sys.argv[2]
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
    if csv_name == '':
        print('Name of the CSV file which will contain the data (press ENTER '
              'to use the default name, "q" to quit): ', end='')
        csv_name = input()
        if csv_name == 'q':
            quit()
        # If the user just hits enter, use default name:
        if csv_name == '':
            csv_name = f'ORCA_data_{inputs_name[:-4]}'

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

    create_csv_from_sds(sd_list, csv_name)
    print(f'Process complete! Results saved as "{csv_name}.csv"')


if __name__ == '__main__':
    main()

