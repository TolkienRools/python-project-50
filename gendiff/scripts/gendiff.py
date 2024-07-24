import argparse
from gendiff import generate_diff


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument('-f', '--format', choices=['stylish', 'plain', 'json'],
                        metavar='FORMAT', help='set format of output',
                        default='stylish')

    return parser.parse_args()


def main():
    args = parse_arguments()

    print(generate_diff(args.first_file, args.second_file,
                        args.format))


if __name__ == '__main__':
    main()
