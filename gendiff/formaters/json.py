import json


def make_json_format(generated):
    return json.dumps(generated, indent=4)
