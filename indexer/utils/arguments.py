import argparse
from parsers import constants


def get_argument_parser():
    """Get argument parser."""
    parser = argparse.ArgumentParser(
        prog='indexer',
        description='The ESV indexer',
        formatter_class=argparse.HelpFormatter,
    )

    parser.add_argument(
        'parser',
        type=str,
        help='which parser to run',
        choices=constants.AVAILABLE_PARSERS,
    )

    parser.add_argument(
        'src',
        type=str,
        help='path to source directory',
    )

    return parser


