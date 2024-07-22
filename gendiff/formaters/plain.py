import itertools


def translate_to_str(value):
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

    if element["type"] == "add":
        return base + (f" was added with value: "
                       f"{translate_to_str(element["value"])}")
    elif element["type"] == "del":
        return base + " was removed"
    else:
        return base + (" was updated. From "
                       f"{translate_to_str(element["old_value"])}"
                       f" to {translate_to_str(element["new_value"])}")


def plain_formatter(generated):
    def iter_(current_value, path=""):

        lines = []

        for element in current_value:

            if path:
                current_property = ".".join([path, element["key"]])
            else:
                current_property = element["key"]

            if element["type"] in ("add", "del", "changed"):
                lines.append(to_format_string(current_property, element))

            elif element["type"] == "nested":

                lines.append(iter_(element["children"], current_property))

        result = itertools.chain(lines)
        return '\n'.join(result)

    return iter_(generated)
