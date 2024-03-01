import os
import json
import sys
from structure_data_builder import StructureDataBuilder


def create_json_from_sds(sd_list, json_name):
    json_dict = {}
    for sd in sd_list:
        sd_data = {'input filename': sd.get_input_filename()}
        for data_section in sd.get_data_sections().values():
            data_section_data = data_section.get_data()
            json_safe_data = {}
            # JSON is not compatible with tuples, so must convert to str
            for key in data_section_data.keys():
                val = data_section_data[key]
                if type(val) == tuple:
                    val = str(val)
                if type(key) == tuple:
                    json_safe_data[str(key)] = val
                else:
                    json_safe_data[key] = val

            sd_data[data_section.get_section_name()] = json_safe_data
        json_dict[sd.get_out_filename()] = sd_data
    with open(f'{json_name}.json', 'w') as f:
        json.dump(json_dict, f, indent=2)


def main():
    # TODO: use an argument parser here instead? make argument inputs more sophisticated?
    json_name = ''
    # process command line arguments
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

    # ask for excel file name
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

