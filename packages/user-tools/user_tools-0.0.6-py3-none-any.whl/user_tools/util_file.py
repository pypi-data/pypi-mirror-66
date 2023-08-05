#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Some functions related to file operations."""
import os
import user_tools.util_time as ut
import user_tools.util_check as uc

SIZE_UNIT = {
    "GB": float(1024*1024*1024),
    "MB": float(1024*1024),
    "KB": float(1024)
}


def write_file(file_path, msg, mode="a", encoding="UTF-8"):
    """Write the contents of msg to file_path.

    :param file_path(str): File to be written.\n
    :param msg(str): What will be written to the file_path.\n
    :param mode(str): How to write file, default is "a".
        Character Meaning
        -----------------------------------
            'w'   open for writing, create if not exists.
                  truncating the file first.
            'x'   create a new file and open it for writing
            'a'   open for writing, create if not exists.
                  appending to the end of the file (default).
            'b'   binary mode.
                  If you use this, no encoding parameter is required
            't'   text mode (default).
            '+'   open a disk file for updating (reading and writing)
    :param encoding(str): Encoding format to write file, default is "UTF-8".\n
    :return(None): No return value."""

    if "b" not in mode:
        with open(file_path, mode, encoding=encoding) as f:
            f.write(msg)
    else:
        with open(file_path, mode) as f:
            f.write(msg)


def read_file(file_path, mode="r", encoding="UTF-8"):
    """Return the content of file_path.

    :param file_path(str): File to be read.\n
    :param mode(str): How to read file, default is "r".
        Character Meaning
        -----------------------------------
            'r'   open for reading (default).
            'b'   binary mode.
                  If you use this, no encoding parameter is required
            't'   text mode (default).
    :param encoding(str): Encoding format to read file, default is "UTF-8".\n
    :return(str): The contents of file_path.
        If the contents of file_path is empty, it may be the following:
            file_path not file; file_path not exist; file_path is null."""

    msg = ""
    expr1 = uc.is_not_null(file_path)
    expr2 = uc.file_or_dir(file_path) == "file"
    if expr1 and expr2:
        if "b" not in mode:
            with open(file_path, mode, encoding=encoding) as f:
                msg = f.read()
        else:
            with open(file_path, mode) as f:
                msg = f.read()
    return msg


def get_file_suffix(filename):
    """Return the suffix of filename.

    :param filename(str): File name to get the suffix.\n
    :return(str): The suffix of filename."""

    return os.path.splitext(filename)[1]


def get_file_size(file_path, size_unit="MB"):
    """Return the size of file_path.

    :param file_path(str): File path to get file size.\n
    :param size_unit(str): File size unit. Default is 'MB'.
        Character Meaning
        -----------------------------------
            'GB'   The file's byte size will be divided by 1024*1024*1024 to get the file size
            'MB'   The file's byte size will be divided by 1024*1024 to get the file size
            'KB'   The file's byte size will be divided by 1024 to get the file size
    :return(float): The size of file_path. Exact to two digits after the decimal point.
        A file size of -1 means the file does not exist."""

    if size_unit in SIZE_UNIT:
        size_unit = SIZE_UNIT[size_unit]
    else:
        size_unit = SIZE_UNIT["MB"]
    file_size = -1
    if uc.is_exist(file_path):
        tmp_size = os.path.getsize(file_path)
        size = tmp_size / size_unit
        file_size = round(size, 2)
    return file_size


def get_file_ctime(file_path, format_str='%Y-%m-%d %H:%M:%S'):
    """Get and format file creation time and return.

    :param file_path(str): File path to get creation time.\n
    :param format_str(str): Time format used to format time.
        Default is '%Y-%m-%d %H:%M:%S'
        Commonly used format codes:
            %Y  Year with century as a decimal number.
            %m  Month as a decimal number [01,12].
            %d  Day of the month as a decimal number [01,31].
            %H  Hour (24-hour clock) as a decimal number [00,23].
            %M  Minute as a decimal number [00,59].
            %S  Second as a decimal number [00,61].
            %z  Time zone offset from UTC.
            %a  Locale's abbreviated weekday name.
            %A  Locale's full weekday name.
            %b  Locale's abbreviated month name.
            %B  Locale's full month name.
            %c  Locale's appropriate date and time representation.
            %I  Hour (12-hour clock) as a decimal number [01,12].
            %p  Locale's equivalent of either AM or PM.
    :return(str): A formatted time string of file_path creation time.
        If the creation time is an empty string, the file does not exist."""

    ctime = ""
    if uc.is_exist(file_path):
        tmp_time = os.path.getctime(file_path)
        ctime = ut.format_time(tmp_time, format_str)
    return ctime


def get_file_atime(file_path, format_str='%Y-%m-%d %H:%M:%S'):
    """Get and format file access time and return.

    :param file_path(str): File path to get access time.\n
    :param format_str(str): Time format used to format time.
        Default is '%Y-%m-%d %H:%M:%S'
        Commonly used format codes:
            %Y  Year with century as a decimal number.
            %m  Month as a decimal number [01,12].
            %d  Day of the month as a decimal number [01,31].
            %H  Hour (24-hour clock) as a decimal number [00,23].
            %M  Minute as a decimal number [00,59].
            %S  Second as a decimal number [00,61].
            %z  Time zone offset from UTC.
            %a  Locale's abbreviated weekday name.
            %A  Locale's full weekday name.
            %b  Locale's abbreviated month name.
            %B  Locale's full month name.
            %c  Locale's appropriate date and time representation.
            %I  Hour (12-hour clock) as a decimal number [01,12].
            %p  Locale's equivalent of either AM or PM.
    :return(str): A formatted time string of file_path access time.
        If the access time is an empty string, the file does not exist."""

    atime = ""
    if uc.is_exist(file_path):
        tmp_time = os.path.getatime(file_path)
        atime = ut.format_time(tmp_time, format_str)
    return atime


def get_file_mtime(file_path, format_str='%Y-%m-%d %H:%M:%S'):
    """Get and format file modification time and return.

    :param file_path(str): File path to get modification time.\n
    :param format_str(str): Time format used to format time.
        Default is '%Y-%m-%d %H:%M:%S'
        Commonly used format codes:
            %Y  Year with century as a decimal number.
            %m  Month as a decimal number [01,12].
            %d  Day of the month as a decimal number [01,31].
            %H  Hour (24-hour clock) as a decimal number [00,23].
            %M  Minute as a decimal number [00,59].
            %S  Second as a decimal number [00,61].
            %z  Time zone offset from UTC.
            %a  Locale's abbreviated weekday name.
            %A  Locale's full weekday name.
            %b  Locale's abbreviated month name.
            %B  Locale's full month name.
            %c  Locale's appropriate date and time representation.
            %I  Hour (12-hour clock) as a decimal number [01,12].
            %p  Locale's equivalent of either AM or PM.
    :return(str): A formatted time string of file_path modification time.
        If the modification time is an empty string, the file does not exist."""

    mtime = ""
    if uc.is_exist(file_path):
        tmp_time = os.path.getmtime(file_path)
        mtime = ut.format_time(tmp_time, format_str)
    return mtime
