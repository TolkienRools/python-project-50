from gendiff.formaters import (make_stylish_format,
                               make_plain_format,
                               make_json_format)
from gendiff.uploaders import load_file


FORMATTERS = {"stylish": make_stylish_format,
              "plain": make_plain_format,
              "json": make_json_format}


def make_inner_element(type, key, first_value, second_value=None):
    if type in ("added", "deleted", "unchanged"):
        return {
            "type": type,
            "key": key,
            "value": first_value
        }
    elif type == "changed":
        return {
            "type": type,
            "key": key,
            "old_value": first_value,
            "new_value": second_value
        }
    else:
        return {
            "type": "nested",
            "key": key,
            "children": first_value
        }


def compare(data1, data2):
    out_store = []

    add_keys = set(data2.keys()) - set(data1.keys())
    del_keys = set(data1.keys()) - set(data2.keys())

    for key in sorted(set(data1.keys()) | set(data2.keys())):
        # add
        if key in add_keys:
            out_store.append(make_inner_element("added", key,
                                                data2[key]))
        # delete
        elif key in del_keys:
            out_store.append(make_inner_element("deleted", key,
                                                data1[key]))
        # nested  (two dicts, call recursion)
        elif (isinstance(data1.get(key), dict)
              and isinstance(data2.get(key), dict)):
            out_store.append(make_inner_element(
                "nested", key,
                compare(data1.get(key), data2.get(key))))
        elif data1.get(key) != data2.get(key):
            out_store.append(make_inner_element("changed", key,
                                                data1[key], data2[key]))
        else:
            out_store.append(make_inner_element("unchanged", key,
                                                data1[key]))

    return out_store


def generate_diff(file1, file2, formatter="stylish"):
    file1 = load_file(file1)
    file2 = load_file(file2)

    inner_repr = compare(file1, file2)
    return FORMATTERS[formatter](inner_repr)
