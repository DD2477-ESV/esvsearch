import pathlib


def create_cache(dir):
    pathlib.Path(dir + '/pdfs').mkdir(parents=True, exist_ok=True)
    pathlib.Path(dir + '/titles').mkdir(parents=True, exist_ok=True)
    pathlib.Path(dir + '/text').mkdir(parents=True, exist_ok=True)
    pathlib.Path(dir + '/dates').mkdir(parents=True, exist_ok=True)
    pathlib.Path(dir + '/download_urls').mkdir(parents=True, exist_ok=True)
