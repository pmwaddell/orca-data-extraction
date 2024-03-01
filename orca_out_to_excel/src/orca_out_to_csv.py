import os
import sys
import pandas as pd
from structure_data_builder import StructureDataBuilder
from orca_out_to_json import make_json_dict


def create_csv_from_sds(sd_list, csv_name):
    json_dict = make_json_dict(sd_list)
    df = pd.json_normalize(json_dict)
    df.to_csv(csv_name + '.csv')


def main():
    # TODO: use an argument parser here instead? make argument inputs more sophisticated?
    csv_name = ''
    # process command line arguments
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

    # ask for excel file name
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

