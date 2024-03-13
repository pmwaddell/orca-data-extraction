#!/usr/bin/env python3
"""
A script to quickly pull desired data from an ORCA .out file and compile
it into an Excel spreadsheet.

Before running, the user should specify what information they want to look for
in a .txt file (see example). When executed, the script checks each file in the
working directory. If the file ends in .out, it exports the desired data into
an excel spreadsheet.
"""
__author__ = "Peter Waddell"
__copyright__ = "Copyright 2024"
__credits__ = ["Peter Waddell"]
__version__ = "0.1.0"
__date__ = "2024/02/28"
__maintainer__ = "Peter Waddell"
__email__ = "pmwaddell9@gmail.com"
__status__ = "Prototype"

import os
import sys
from structure_data_builder import StructureDataBuilder
from xlwt import Workbook


def create_excel_from_sds(sd_list, excel_name):
    """
    Uses Workbook to create an excel file and populate the first sheet with the
    desired set of data from the ORCA .out files in the directory, which
    are passed in the form of the dictionary sd_list.

    Parameters
    ----------
    sd_list : list
        List containing the set of StructureData instances that each come
        from the ORCA .out files.
    excel_name : str
        Desired name of the excel file that will store the data.
    """
    def write_sd_to_excel(current_sd, current_sheet, current_count):
        """
        Writes the data from an instance of StructureData into the desired sheet
        of the Workbook instance.

        Parameters
        ----------
        current_sd : object (StructureData)
            The instance of StructureData whose information is being used to
            write to excel for this function call.
        current_sheet : object
            The sheet object that will be written to, from a particular instance
            of a Workbook.
        current_count : int
            The value of count from the enumerate of the for loop that iterates
            through all the instances of StructureData objects in sd_list. It is
            really only used for when it is 0, which indicates that column
            headers should be written in to the excel sheet.
        """
        def write_datum_to_excel(datum_label, datum, sheet):
            """
            Writes a piece of data ('datum') from a DataSection instance into
            the excel spreadsheet.

            Parameters
            ----------
            datum_label : str
                String describing the piece of data to be written into excel.

            datum : str or dict
                This variable contains the information that will be written into
                the excel file, either as an individual string of a number
                (e.g. for a bond length) or a dictionary containing several
                associated values for a particular atom (e.g. for input
                coordinates data).

            sheet : object
                Sheet from the workbook instance (from xlwt) to which the data
                is written.
            """
            # Depending on the data section, data will be either a dictionary
            # or a string of a numerical value, so these cases are handled
            # separately.
            nonlocal column
            if type(datum) is dict:
                for elem in datum:
                    # Add atom labels in the top row, only the first time:
                    if current_count == 0:
                        sheet.write(row - 1, column, f'{datum_label} {elem}')
                    sheet.write(row, column, f'{datum[elem]}')
                    column += 1
            else:
                if current_count == 0:
                    sheet.write(row - 1, column, f'{datum_label}')
                sheet.write(row, column, f'{datum}')
                column += 1

        def write_data_section(column_title, section_data):
            """
            Writes the data from a particular DataSection into the spreadsheet.

            Parameters
            ----------
            column_title : str
                Name of the data section, which will be the title of the column
                in the excel spreadsheet.
            section_data : str or dict
                Data to be written to excel for the data section, either in the
                form of a single str or a dict mapping str to str, depending on
                how the data is structured.
            """
            # Add column titles in the top row, only the first time:
            if current_count == 0:
                current_sheet.write(0, column, column_title)
            for datum_label in section_data:
                write_datum_to_excel(datum_label, section_data[datum_label],
                                     current_sheet)

        column = 1
        # Add .out filename to spreadsheet.
        current_sheet.write(row, 0, current_sd.get_out_filename())

        current_data_sections = current_sd.get_data_sections()
        for data_section_name in current_data_sections:
            write_data_section(
                data_section_name,
                current_sd.get_data_section(data_section_name).get_data())

    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')
    row = 2
    for count, sd in enumerate(sd_list):
        write_sd_to_excel(sd, sheet1, count)
        row += 1
    wb.save(f'{excel_name}.xls')


def main():
    # TODO: use an argument parser here instead? make argument inputs more sophisticated?
    excel_name = ''
    # Process command line arguments
    if len(sys.argv) >= 2:
        inputs_name = sys.argv[1]
        if not os.path.isfile(inputs_name):
            print('No file with name ' + inputs_name + ' found.')
            quit()
        if len(sys.argv) >= 3:
            excel_name = sys.argv[2]
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
    if excel_name == '':
        print('Name of the Excel file which will contain the data (press ENTER '
              'to use the default name, "q" to quit): ', end='')
        excel_name = input()
        if excel_name == 'q':
            quit()
        # If the user just hits enter, use default name:
        if excel_name == '':
            excel_name = f'ORCA_data_{inputs_name[:-4]}'

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

    create_excel_from_sds(sd_list, excel_name)
    print(f'Process complete! Results saved as "{excel_name}.xls"')


if __name__ == '__main__':
    main()
