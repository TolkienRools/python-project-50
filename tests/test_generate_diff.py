import pytest
from pathlib import Path
from gendiff import generate_diff

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def open_file(path):
    with open(path, "r") as stream:
        return stream.read()


@pytest.mark.parametrize("first,second,expected,format",
                         [("first_flat.json", "second_flat.json",
                           "out_flat_stylish.txt", "stylish"),
                          ("first_flat.yml", "second_flat.yml",
                           "out_flat_stylish.txt", "stylish"),
                          ("first_deep.json", "second_deep.json",
                           "out_deep_stylish.txt", "stylish"),
                          ("first_deep.yml", "second_deep.yml",
                           "out_deep_stylish.txt", "stylish"),
                          ("first_flat.json", "second_flat.json",
                           "out_flat_plain.txt", "plain"),
                          ("first_flat.yml", "second_flat.yml",
                           "out_flat_plain.txt", "plain"),
                          ("first_deep.json", "second_deep.json",
                           "out_deep_plain.txt", "plain"),
                          ("first_deep.yml", "second_deep.yml",
                           "out_deep_plain.txt", "plain"),
                          ("first_flat.json", "second_flat.json",
                           "out_flat_json.txt", "json"),
                          ("first_flat.yml", "second_flat.yml",
                           "out_flat_json.txt", "json"),
                          ("first_deep.json", "second_deep.json",
                           "out_deep_json.txt", "json"),
                          ("first_deep.yml", "second_deep.yml",
                           "out_deep_json.txt", "json")
                          ])
def test_generate_diff_stylish(first, second, expected, format):
    first_in = FIXTURES_DIR / first
    second_in = FIXTURES_DIR / second
    expected_txt = open_file(FIXTURES_DIR / expected)

    result = generate_diff(first_in, second_in, format)

    assert result == expected_txt
