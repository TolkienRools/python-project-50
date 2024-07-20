import argparse
from gendiff import generate_diff, stylish, upload_file


def main():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument('-f', '--format', metavar='FORMAT',
                        help='set format of output')

    args = parser.parse_args()


    first_file = upload_file(args.first_file)
    second_file = upload_file(args.second_file)

    inner = generate_diff(first_file, second_file)

    print(stylish(inner))


if __name__ == '__main__':
    main()
