

def func1(var):
    if isinstance(var, str):
        return "string"
    if isinstance(var, int):
        return "number"

    return "else"