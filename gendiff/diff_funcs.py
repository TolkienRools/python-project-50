import json
from collections import OrderedDict
import os

def translate_to_json(value):
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return "null"

    return value

def stringify(data, spaceholder=" ", spacer_repeat=1):

    def inner_repeat(data, depth=1):

        if not isinstance(data, dict):
            return translate_to_json(data)

        spaces_number = depth * spacer_repeat - 2
        spaces_number_end = (depth - 1) * spacer_repeat

        result_string = "{\n"
        for key, value in data.items():
            result_string += ((spaceholder * spaces_number) +
                              f"{key[0]} {key[1]}: {inner_repeat(value, depth+1)}\n")
        result_string += (spaceholder * spaces_number_end) + "}"

        return result_string

    return inner_repeat(data)


def generate_diff(file_path1, file_path2):
    file1 = json.load(open(os.path.normpath(os.path.join(os.getcwd(),file_path1))))
    file2 = json.load(open(os.path.normpath(os.path.join(os.getcwd(),file_path2))))


    def inner_(data):

        if not isinstance(data, tuple):
            if isinstance(data, dict):
                return {(" ", key): inner_(value) for key, value in data.items()}
            else:
                return data

        data1, data2 = data

        out_dict = OrderedDict()

        first_file_keys = set(data1.keys()) - set(data2.keys())
        shared_file_keys = set(data1.keys()) & set(data2.keys())

        for key in sorted(set(data1.keys()) | set(data2.keys())):

            if key in first_file_keys:
                out_dict[("-", key)] = inner_(data1[key])

            elif key in shared_file_keys:

                if isinstance(data1[key], dict) and isinstance(data2[key], dict):
                    out_dict[(" ", key)] = inner_((data1[key], data2[key]))
                else:
                    if data1[key] == data2[key]:
                        out_dict[(" ", key)] = inner_(data1[key])
                    else:
                        out_dict[("-", key)] = inner_(data1[key])
                        out_dict[("+", key)] = inner_(data2[key])
            else:
                out_dict[("+", key)] = inner_(data2[key])

        return out_dict

    return inner_((file1, file2))
