import itertools


def format_value(value):
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return "null"

    if isinstance(value, dict):
        return "[complex value]"

    if isinstance(value, (int, float)):
        return value

    return f"'{value}'"


def to_format_string(property, element):
    base = f"Property '{property}'"

    if element['type'] == "added":
        return base + (" was added with value: "
                       f"{format_value(element['value'])}")
    elif element['type'] == "deleted":
        return base + " was removed"
    else:
        return base + (" was updated. From "
                       f"{format_value(element['old_value'])}"
                       f" to {format_value(element['new_value'])}")


def make_plain_format(generated):
    def iter_(current_value, path=""):

        lines = []

        for element in current_value:

            if path:
                current_property = ".".join([path, element['key']])
            else:
                current_property = element['key']

            if element['type'] in ("added", "deleted", "changed"):
                lines.append(to_format_string(current_property, element))

            elif element['type'] == "nested":

                lines.append(iter_(element['children'], current_property))

        result = itertools.chain(lines)
        return '\n'.join(result)

    return iter_(generated)
