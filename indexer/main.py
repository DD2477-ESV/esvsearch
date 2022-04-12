import sys
from utils import arguments
from parsers import constants
from parsers import riksdagen


def main():
    parser = arguments.get_argument_parser()
    args = parser.parse_args(sys.argv[1:])

    if args.parser == constants.RIKSDAGEN:
        riksdagen.parse(args)


if __name__ == '__main__':
    main()
