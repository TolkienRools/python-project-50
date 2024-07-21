import argparse
from gendiff import generate_diff, upload_file


def main():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument('-f', '--format', choices=['stylish', 'plain', 'json'],
                        metavar='FORMAT', help='set format of output',
                        default='stylish')

    args = parser.parse_args()

    first_file = upload_file(args.first_file)
    second_file = upload_file(args.second_file)

    print(generate_diff(first_file, second_file, args.format))


if __name__ == '__main__':
    main()
