from . import indexer


def parse(args):
    indexer.walk_and_index_all_files(args.src)
