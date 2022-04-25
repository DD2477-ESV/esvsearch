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
    esv,
    polisen,
    pts,
    fi,
    riksbanken,
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
    elif args.parser == constants.ESV:
        esv.parse(args)
    elif args.parser == constants.POLISEN:
        polisen.parse(args)
    elif args.parser == constants.PTS:
        pts.parse(args)
    elif args.parser == constants.FI:
        fi.parse(args)
    elif args.parser == constants.RIKSBANKEN:
        riksbanken.parse(args)


if __name__ == '__main__':
    main()
