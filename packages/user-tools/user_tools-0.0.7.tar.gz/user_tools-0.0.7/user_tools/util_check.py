#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Some checks on files or directories."""
import os
import re


def is_exist(file_path, create=False):
    """Test whether file_path exists.

    :param file_path(str): The path that needs to be judged.\n
    :param create(bool): Whether to create.
        If create is True, create a directory named file_path if it does not exist.
    :return(bool): A boolean representing whether file_path exists."""

    if create and not os.path.exists(file_path):
        os.makedirs(file_path)
    return os.path.exists(file_path)


def is_not_null(file_path):
    """Test whether file_path is not null.

    :param file_path(str): The path that needs to be judged.\n
    :return(bool): Returns whether file_path is not null.
        Return True if file_path exist and not null.
        Return False, it may be the following:
            file_path not file or dir; file_path not exist."""

    result = False
    if is_exist(file_path):
        if file_or_dir(file_path) == "file":
            result = os.path.getsize(file_path) != 0
        elif file_or_dir(file_path) == "dir":
            result = bool(os.listdir(file_path))
    return result


def file_or_dir(file_path):
    """ Returns file type of the file_path.

    :param file_path(str): The path that needs to be judged.\n
    :return(str): Returns file type of the file_path.
        The return values are as follows.
            "dir": If file_path is a directory,
            "file": If file_path is a file,
            "": If file_path is not exist or not a dir or file."""

    result = ""
    if os.path.isdir(file_path):
        result = "dir"
    elif os.path.isfile(file_path):
        result = "file"
    return result


def check_url(url, style="web"):
    """Test whether url is valid.

    this way is not finished
    ==

    :params url(str): The url that needs to be judged.\n
    :return(bool): Returns whether url is valid.
        Return False, if the style is not web or git.
    """

    result = False
    if style == "web":
        result = re.match(r'^https?:/{2}\w.+$', url)
    elif style == "git":
        pass
    return result
