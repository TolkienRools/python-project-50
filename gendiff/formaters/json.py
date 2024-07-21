import json


def json_formatter(generated):
    return json.dumps(generated, indent=4, separators=(',', ': '))
