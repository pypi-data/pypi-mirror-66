#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Some functions related to json file operations."""
import json
from user_tools import util_check as uc


def read_json(json_file):
    """Return the contents of json_file.

    :param json_file(str): Json file to be read.\n
    :return(dict): the contents of json_file.
        If the return value is empty, it may be the following:
            json_file not file; json_file not exist; json_file is null."""

    json_dict = {}
    expr1 = uc.is_not_null(file_path)
    expr2 = uc.file_or_dir(file_path) == "file"
    if expr1 and expr2:
        with open(json_file, "r", encoding="UTF-8") as f:
            json_dict = json.load(f)
    return json_dict


def write_json(json_file, json_dict, mode="w"):
    """Write the contents of json_dict to json_file.

    :param json_file(str): Json file to be written.\n
    :param json_dict(str): What will be written to the json file.\n
    :param mode(str): How to write json file, default is "w".
        Character Meaning
        -----------------------------------
            'w'   open for writing, create if not exists.
                  truncating the file first.
            'x'   create a new file and open it for writing
            'a'   open for writing, create if not exists.
                  appending to the end of the file.
            'b'   binary mode.
                  If you use this, no encoding parameter is required
            't'   text mode (default)
            '+'   open a disk file for updating (reading and writing)
    :return(None): No return value."""

    with open(json_file, mode, encoding="UTF-8") as f:
        # ensure_ascii = False is to display Chinese,
        # if not written, it will be displayed as unicode encoding.
        # indent is to format the json file,
        # otherwise it will be displayed on one line.
        json.dump(json_dict, f, ensure_ascii=False, indent=4)
