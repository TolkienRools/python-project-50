import pytest
from pathlib import Path
from gendiff import generate_diff, stylish, upload_file


FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize("first,second,expected",
                         [("first_flat.json", "second_flat.json",
                           "out_flat.txt"),
                          ("first_flat.yml", "second_flat.yml",
                           "out_flat.txt"),
	                      ("first_deep.json", "second_deep.json",
                           "out_deep.txt"),
	                      ("first_deep.yml", "second_deep.yml",
	                       "out_deep.txt")])
def test_generate_diff(first, second, expected):
	first_in = upload_file(FIXTURES_DIR / first)
	second_in = upload_file(FIXTURES_DIR / second)
	expected_txt = upload_file(FIXTURES_DIR / expected)

	inner_state = generate_diff(first_in, second_in)
	result = stylish(inner_state)

	assert result == expected_txt
