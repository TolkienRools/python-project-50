import itertools

SEPARATOR = " "
INDENT = 2
SIGNS_CONVERT = {"added": "+", "deleted": "-", "unchanged": " "}
SPACES = 4


def format_dict(inner_value, depth, recursive_callable):
    specer_size = depth * SPACES
    deep_indent = SEPARATOR * (specer_size - INDENT)
    current_indent = SEPARATOR * (specer_size - SPACES)

    lines = []

    for key, value in inner_value.items():
        tranlated_value = format_value(value, depth + 1)
        lines.append(f'{deep_indent}  {key}: {tranlated_value}')

    result = itertools.chain("{", lines, [current_indent + "}"])
    return '\n'.join(result)


def format_value(inner_value, depth=1):
    if isinstance(inner_value, bool):
        return str(inner_value).lower()
    if inner_value is None:
        return "null"

    if isinstance(inner_value, dict):

        return format_dict(inner_value, depth,
                           format_value)

    return inner_value


def tree_stylization(current_value, depth):
    if not isinstance(current_value, list):
        return str(current_value)

    specer_size = depth * SPACES
    deep_indent = SEPARATOR * (specer_size - INDENT)
    current_indent = SEPARATOR * (specer_size - SPACES)

    lines = []

    for element in current_value:

        if element['type'] in ("added", "deleted", "unchanged"):
            value = format_value(element['value'],
                                 depth + 1)

            lines.append(f"{deep_indent}{SIGNS_CONVERT[element['type']]}"
                         f" {element['key']}: {value}")

        elif element['type'] == "changed":
            old_value = format_value(element['old_value'],
                                     depth + 1)
            new_value = format_value(element['new_value'],
                                     depth + 1)
            lines.append(f"{deep_indent}{SIGNS_CONVERT['deleted']} "
                         f"{element['key']}: {old_value}")
            lines.append(f"{deep_indent}{SIGNS_CONVERT['added']} "
                         f"{element['key']}: {new_value}")

        elif element['type'] == "nested":
            lines.append(f"{deep_indent}{SIGNS_CONVERT['unchanged']} "
                         f"{element['key']}:"
                         f" {tree_stylization(element['children'], depth + 1)}")

    result = itertools.chain("{", lines, [current_indent + "}"])
    return '\n'.join(result)


def make_stylish_format(generated):
    return tree_stylization(generated, 1)
