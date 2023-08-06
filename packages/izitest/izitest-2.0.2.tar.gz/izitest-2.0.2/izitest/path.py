# coding: utf-8

from typing import (List, TextIO)

import os
from sys import stdout, stderr
from pathlib import Path

from .betterprint import printerror

__all__ = [
    "check_file",
    "check_exec",
    "check_dir"
]


def check_file(path: Path):
    """Check if given path points to a regular file.

    Args:
        path (Path): path to check

    Raises:
        Exception: if not a regular file
    """
    if not path.is_file():
        printerror(f"{path} is not a valid file!")
        raise Exception


def check_exec(path: Path):
    """Check if given path points to a regular file.

    Args:
        path (Path): path to check

    Raises:
        Exception: if not a regular file
    """
    if not os.access(path, os.X_OK):
        printerror(f"{path} is not executable!")
        raise Exception


def check_dir(path: Path):
    """Check if given path points to a regular file.

    Args:
        path (Path): path to check

    Raises:
        Exception: if not a regular file
    """
    if not path.is_dir():
        printerror(f"{path} is not a valid directory!")
        raise Exception
