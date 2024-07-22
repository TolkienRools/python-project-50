import itertools


SEPARATOR = " "
INDENT = 2
SIGNS_CONVERT = {"add": "+", "del": "-", "unchanged": " "}
SPACES = 4


def translate_to_simple(inner_value, depth=1):
    if isinstance(inner_value, bool):
        return str(inner_value).lower()
    if inner_value is None:
        return "null"

    if isinstance(inner_value, dict):

        specer_size = depth * SPACES
        deep_indent = SEPARATOR * (specer_size - INDENT)
        current_indent = SEPARATOR * (specer_size - SPACES)

        lines = []

        for key, value in inner_value.items():
            tranlated_value = translate_to_simple(value, depth + 1)
            lines.append(f'{deep_indent}  {key}: {tranlated_value}')

        result = itertools.chain("{", lines, [current_indent + "}"])
        return '\n'.join(result)

    return inner_value


def tree_stylization(current_value, depth):
    if not isinstance(current_value, list):
        return str(current_value)

    specer_size = depth * SPACES
    deep_indent = SEPARATOR * (specer_size - INDENT)
    current_indent = SEPARATOR * (specer_size - SPACES)

    lines = []

    for element in current_value:

        if element["type"] in ("add", "del", "unchanged"):
            value = translate_to_simple(element["value"],
                                        depth + 1)

            lines.append(f'{deep_indent}{SIGNS_CONVERT[element["type"]]}'
                         f' {element["key"]}: {value}')

        elif element["type"] == "changed":
            old_value = translate_to_simple(element["old_value"],
                                            depth + 1)
            new_value = translate_to_simple(element["new_value"],
                                            depth + 1)
            lines.append(f'{deep_indent}- {element["key"]}: {old_value}')
            lines.append(f'{deep_indent}+ {element["key"]}: {new_value}')

        elif element["type"] == "nested":
            lines.append(f'{deep_indent}  {element["key"]}:'
                         f' {tree_stylization(element["children"], depth + 1)}')

    result = itertools.chain("{", lines, [current_indent + "}"])
    return '\n'.join(result)


def stylish_formatter(generated):
    return tree_stylization(generated, 1)
