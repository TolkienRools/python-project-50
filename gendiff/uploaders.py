import json
import yaml
from pathlib import Path


def upload_file(file):
    path_to_file = Path(file)

    with open(path_to_file, 'r') as stream:
        if path_to_file.suffix == '.json':
            return json.load(stream)

        elif path_to_file.suffix in ('.yml', '.yaml'):
            return yaml.safe_load(stream)

        return stream.read()
