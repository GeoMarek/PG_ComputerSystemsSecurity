import os


def init_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return dirname
