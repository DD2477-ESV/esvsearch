from dateutil.parser import parse


def is_date(string, fuzzy=False):
    try:
        parse(string, fuzzy=fuzzy)
        # exclude dates shorter than 5 chars, to
        # try to find the first date with not just a year
        if len(string) < 5:
            return False
        if sum(c.isdigit() for c in string) < 5:
            return False
        return True
    except ValueError:
        return False
