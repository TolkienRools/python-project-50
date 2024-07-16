import json
import os
import itertools


def translate_to_json(value):
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return "null"

    # обработка, если словарь, поможет с теми, что сейчас плоские 

    return value


# def single_value_tree(simple_dict, depth, spaces_count, replacer, indent):
#
#     if not isinstance(simple_dict, dict):
#         return str(simple_dict)
#
#     lines = []
#     specer_size = depth * spaces_count
#     current_indent = replacer * depth
#
#     for key, value in simple_dict.items():
#         deep_indent = replacer * (specer_size - indent)
#         lines.append(f'{deep_indent}  {key}: {single_value_tree(value, depth, spaces_count, replacer, indent)}')
#
#     result = itertools.chain("{", lines, [current_indent + "}"])
#     return '\n'.join(result)


def json_stringify(generated, replacer=' ', spaces_count=4):

    indent = 2

    def iter_(current_value, depth):
        # if isinstance(current_value, dict):
        #     return single_value_tree(current_value, depth, spaces_count, replacer, indent)
        if not isinstance(current_value, list):
            return str(current_value)

        # deep_indent_size = depth + spaces_count
        specer_size = depth * spaces_count
        current_indent = replacer * (depth * spaces_count)
        lines = []

        # print("LEVEL", depth, generated)
        # Создать проход по циклу
        for element in current_value:

            if element["type"] == "add":
                deep_indent = replacer * (specer_size - indent)
                lines.append(f'{deep_indent}+ {element["key"]}: {element["value"]}')

            if element["type"] == "del":
                deep_indent = replacer * (specer_size - indent)
                lines.append(f'{deep_indent}- {element["key"]}: {element["value"]}')

            if element["type"] == "unchanged":
                deep_indent = replacer * (specer_size - indent)
                lines.append(f'{deep_indent}  {element["key"]}: {element["value"]}')

            if element["type"] == "changed":
                deep_indent = replacer * (specer_size - indent)
                lines.append(f'{deep_indent}- {element["key"]}: {element["old_value"]}')
                lines.append(f'{deep_indent}+ {element["key"]}: {element["new_value"]}')

            if element["type"] == "nested":
                deep_indent = replacer * (specer_size - indent)
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
        # shared_keys = set(data1.keys()) & set(data2.keys())

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
