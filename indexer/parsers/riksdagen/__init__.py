from . import indexer


def parse(args):
    indexer.index_all_files(args.src)
