"""
A collection of useful functions that work on paths
"""

import json
import os
from typing import Dict


def init_directory(dirname: str) -> str:
    """
    Init directory if not exist and return its path
    """
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return dirname


def init_config() -> Dict[str, str]:
    """
    Read data from 'config.json' and return dictionary form its pairs
    """
    with open(os.path.join(os.getcwd(), "config.json")) as file:
        return json.load(file)


def init_style() -> str:
    """
    Read data from 'style.css' and return this data
    """
    with open(os.path.join(os.getcwd(), "style.css")) as styles:
        return styles.read()
