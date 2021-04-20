import json
import os


def init_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return dirname


def init_config():
    with open(os.path.join(os.getcwd(), "config.json")) as file:
        return json.load(file)


def init_style():
    with open(os.path.join(os.getcwd(), "GUI", "style.css")) as styles:
        return styles.read()
