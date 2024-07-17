import pytest
from pathlib import Path
from gendiff.diff_funcs import generate_diff, json_stringify

FIXTURES_DIR = Path(__file__).parent / "fixtures"

def get_output_string(out_file_name):
	with open(FIXTURES_DIR / out_file_name, 'r') as f:
		result = f.read()

	return result


@pytest.mark.parametrize("first_json,second_json,expected",
                         [("first_flat.json", "second_flat.json",
                           "out_flat.txt"),
	                      ("first_deep.json", "second_deep.json",
                           "out_deep.txt")])
def test_generate_diff(first_json, second_json, expected):
	first_json_in = FIXTURES_DIR / first_json
	second_json_in = FIXTURES_DIR / second_json
	expected_txt = FIXTURES_DIR / expected

	inner_state = generate_diff(first_json_in, second_json_in)
	result = json_stringify(inner_state)

	assert result == get_output_string(expected_txt)
