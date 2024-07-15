import json
import os
import itertools


def translate_to_json(value):
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return "null"

    return value


def json_stringify(generated, replacer=' ', spaces_count=1):

    def iter_(current_value, depth):
        if not isinstance(current_value, list):
            return str(current_value)

        deep_indent_size = depth + spaces_count
        deep_indent = replacer * deep_indent_size
        current_indent = replacer * depth
        lines = []

        # Создать проход по циклу
        for element in generated:
            if element["type"] in ("add", "del", "unchanged"):
                print(element["type"])
                lines.append(f'{deep_indent}{element["key"]}: {iter_(element["value"], deep_indent_size)}')
        result = itertools.chain("{", lines, [current_indent + "}"])
        return '\n'.join(result)

    return iter_(generated, 0)


def generate_diff(file_path1, file_path2):
    file1 = json.load(open(file_path1, "r"))
    file2 = json.load(open(file_path2, "r"))

    def inner_(data1, data2):

        out_store = []

        add_keys = set(data2.keys()) - set(data1.keys())
        del_keys = set(data1.keys()) - set(data2.keys())
        shared_keys = set(data1.keys()) & set(data2.keys())

        for key in sorted(set(data1.keys()) | set(data2.keys())):
            # add
            if key in add_keys:
                out_store.append({
                    "type": "add",
                    "key": key,
                    "value": data2[key]
                })

            # delete
            if key in del_keys:
                out_store.append({
                    "type": "del",
                    "key": key,
                    "value": data1[key]
                })

            # nested  (two dicts, call recursion)
            if isinstance(data1.get(key), dict) and isinstance(data2.get(key), dict):
                out_store.append({
                    "type": "nested",
                    "key": key,
                    "children": inner_(data1.get(key), data2.get(key))
                })

            if key in shared_keys:
                # unchanged
                if data1.get(key) == data2.get(key):
                    out_store.append({
                        "type": "unchanged",
                        "key": key,
                        "value": data1[key]
                    })
                # changed
                if data1.get(key) != data2.get(key):
                    out_store.append({
                        "type": "changed",
                        "key": key,
                        "old_value": data1[key],
                        "new_value": data2[key]
                    })

        return out_store

    return inner_(file1, file2)


print(generate_diff('gendiff/file1.json', 'gendiff/file2.json'))
print(json_stringify(generate_diff('gendiff/file1.json', 'gendiff/file2.json')))
