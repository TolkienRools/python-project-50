import pytest
from gendiff.diff_funcs import generate_diff, json_stringify


def get_output_string(path):
	with open(path, 'r') as f:
		result = f.read()

	return result


def test_bla_bla():
	pass

# def test_generate_diff_deep():
# 	path_json_in_1 = 'fixtures/input/file1.json'
# 	path_json_in_2 = 'fixtures/input/file2.json'
# 	path_txt_out = 'fixtures/output/deep_diff_result.txt'
#
# 	assert generate_diff(
# 		path_json_in_1,
# 	    path_json_in_2) == get_output_string(path_txt_out)

def test_generate_diff_flat():
	path_json_in_1 = 'tests/fixtures/first_flat.json'
	path_json_in_2 = 'tests/fixtures/second_flat.json'
	path_txt_out = 'tests/fixtures/out_flat.txt'

	inner_state = generate_diff(path_json_in_1, path_json_in_2)
	result = json_stringify(inner_state)

	assert result == get_output_string(path_txt_out)