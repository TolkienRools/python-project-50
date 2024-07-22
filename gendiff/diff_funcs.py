from .formaters import (stylish_formatter,
                        plain_formatter,
                        json_formatter)

FORMATTERS = {"stylish": stylish_formatter,
              "plain": plain_formatter,
              "json": json_formatter}


def make_inner_element(type, key, first_value, second_value=None):

    if type in ("add", "del", "unchanged"):
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
            out_store.append(make_inner_element("add", key,
                                                data2[key]))
        # delete
        elif key in del_keys:
            out_store.append(make_inner_element("del", key,
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


def generate_diff(first_file, second_file, formatter="stylish"):
    inner_repr = compare(first_file, second_file)
    return FORMATTERS[formatter](inner_repr)
