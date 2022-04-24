import sys


def log(var, end=None):
    """Print.

    Wrapper around print.

    Args:
        var: some variable
        end: end of line character (default: {None})
    """
    if end is not None:
        print(var, end=end)
    else:
        print(var)
    sys.stdout.flush()


def eol():
    """Print end of line character."""
    log('')
