import json
import os
import itertools


SEPARATOR = " "


def translate_to_simple(inner_value, depth=1, spaces_count=4, indent=2):
    if isinstance(inner_value, bool):
        return str(inner_value).lower()
    if inner_value is None:
        return "null"

    if isinstance(inner_value, dict):

        specer_size = depth * spaces_count
        deep_indent = SEPARATOR * (specer_size - indent)
        current_indent = SEPARATOR * (specer_size - spaces_count)

        lines = []

        for key, value in inner_value.items():
            tranlated_value = translate_to_simple(value, depth+1,
                                                  spaces_count,
                                                  indent)
            lines.append(f'{deep_indent}  {key}: {tranlated_value}')

        result = itertools.chain("{", lines, [current_indent + "}"])
        return '\n'.join(result)

    return inner_value


def json_stringify(generated, spaces_count=4):

    indent = 2

    def iter_(current_value, depth):
        if not isinstance(current_value, list):
            return str(current_value)

        specer_size = depth * spaces_count
        deep_indent = SEPARATOR * (specer_size - indent)
        current_indent = SEPARATOR * (specer_size - spaces_count)

        lines = []

        for element in current_value:

            if element["type"] in ("add", "del", "unchanged"):
                value = translate_to_simple(element["value"],
                                            depth + 1, spaces_count,
                                            indent)

                if element["type"] == "add":
                    lines.append(f'{deep_indent}+ {element["key"]}: {value}')

                elif element["type"] == "del":
                    lines.append(f'{deep_indent}- {element["key"]}: {value}')

                elif element["type"] == "unchanged":
                    lines.append(f'{deep_indent}  {element["key"]}: {value}')

            elif element["type"] == "changed":
                old_value = translate_to_simple(element["old_value"],
                                                depth + 1, spaces_count,
                                                indent)
                new_value = translate_to_simple(element["new_value"],
                                                depth + 1, spaces_count,
                                                indent)
                lines.append(f'{deep_indent}- {element["key"]}: {old_value}')
                lines.append(f'{deep_indent}+ {element["key"]}: {new_value}')

            elif element["type"] == "nested":
                lines.append(f'{deep_indent}  {element["key"]}: {iter_(element["children"], depth + 1)}')

        result = itertools.chain("{", lines, [current_indent + "}"])
        return '\n'.join(result)

    return iter_(generated, 1)


def generate_diff(file_path1, file_path2):
    file1 = json.load(open(file_path1, "r"))
    file2 = json.load(open(file_path2, "r"))

    def inner_(data1, data2):

        out_store = []

        add_keys = set(data2.keys()) - set(data1.keys())
        del_keys = set(data1.keys()) - set(data2.keys())

        for key in sorted(set(data1.keys()) | set(data2.keys())):
            # add
            if key in add_keys:
                out_store.append({
                    "type": "add",
                    "key": key,
                    "value": data2[key]
                })

            # delete
            elif key in del_keys:
                out_store.append({
                    "type": "del",
                    "key": key,
                    "value": data1[key]
                })

            # nested  (two dicts, call recursion)
            elif isinstance(data1.get(key), dict) and isinstance(data2.get(key), dict):
                out_store.append({
                    "type": "nested",
                    "key": key,
                    "children": inner_(data1.get(key), data2.get(key))
                })

            elif data1.get(key) != data2.get(key):
                out_store.append({
                    "type": "changed",
                    "key": key,
                    "old_value": data1[key],
                    "new_value": data2[key]
                })

            else:
                out_store.append({
                    "type": "unchanged",
                    "key": key,
                    "value": data1[key]
                })

        return out_store

    return inner_(file1, file2)


print(generate_diff('gendiff/file1.json', 'gendiff/file2.json'))
print(json_stringify(generate_diff('gendiff/file1.json', 'gendiff/file2.json')))
