#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Custom random function."""
import random


def random_str(str):
    """Randomly shuffle strings."""
    list_str = list(str)
    random.shuffle(list_str)
    return list_str
