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
            tranlated_value = translate_to_simple(value, depth + 1,
                                                  spaces_count,
                                                  indent)
            lines.append(f'{deep_indent}  {key}: {tranlated_value}')

        result = itertools.chain("{", lines, [current_indent + "}"])
        return '\n'.join(result)

    return inner_value


def stylish(generated, spaces_count=4):

    indent = 2

    signs_convert = {"add": "+", "del": "-", "unchanged": " "}

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

                lines.append(f'{deep_indent}{signs_convert[element["type"]]}'
                             f' {element["key"]}: {value}')

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
                lines.append(f'{deep_indent}  {element["key"]}:'
                             f' {iter_(element["children"], depth + 1)}')

        result = itertools.chain("{", lines, [current_indent + "}"])
        return '\n'.join(result)

    return iter_(generated, 1)