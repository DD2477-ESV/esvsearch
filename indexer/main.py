import sys
from utils import arguments
from parsers import constants
from parsers import (
    riksdagen,
    arbetsformedlingen,
    bra,
    msb,
    fhm,
    forsakringskassan,
)


def main():
    parser = arguments.get_argument_parser()
    args = parser.parse_args(sys.argv[1:])

    if args.parser == constants.RIKSDAGEN:
        riksdagen.parse(args)
    elif args.parser == constants.ARBETSFORMEDLINGEN:
        arbetsformedlingen.parse(args)
    elif args.parser == constants.BRA:
        bra.parse(args)
    elif args.parser == constants.MSB:
        msb.parse(args)
    elif args.parser == constants.FHM:
        fhm.parse(args)
    elif args.parser == constants.FORSAKRINGSKASSAN:
        forsakringskassan.parse(args)


if __name__ == '__main__':
    main()
