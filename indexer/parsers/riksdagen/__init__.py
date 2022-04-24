from . import indexer


def parse(args):
    index_name = 'riksdagen'
    indexer.configure_index(index_name)
    indexer.walk_and_index_all_files(args.src, index_name)
