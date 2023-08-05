#!/usr/bin/env python3
################################################################################
# Name:         CJK Format
# Repository:   https://github.com/HuidaeCho/cjkformat
# Requires:     re, unicodedata
# Author:       Huidae Cho
# Since:        April 15, 2020
#
# Copyright (C) 2020, Huidae Cho <https://idea.isnew.info>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
################################################################################

import re
import unicodedata

def width(s):
    '''
    Returns the display width of a string that may include wide CJK
    characters.

    Arguments:
        s (str): string

    Returns:
        Display length of s (int)
    '''
    # https://www.programcreek.com/python/example/5938/unicodedata.east_asian_width
    # https://sarc.io/development/810-python-print-format-padding
    return sum(1 + (unicodedata.east_asian_width(c) in 'WF') for c in s)

def wide_count(s):
    '''
    Returns the number of wide CJK characters in a string.

    Arguments:
        s (str): string

    Returns:
        Number of wide CJK characters (int)
    '''
    return sum(unicodedata.east_asian_width(c) in 'WF' for c in s)

def f(fmt, *args):
    '''
    Adjusts fixed-width string specifiers for wide CJK characters and returns a
    formatted string.

    Arguments:
        fmt (str): format string
        *args: arguments for the format string

    Returns:
        Formatted string (str)
    '''
    matches = []
    # https://docs.python.org/3/library/stdtypes.html#old-string-formatting
    for m in re.finditer('%([#0 +-]*)([0-9]*)(\.[0-9]*)?([hlL]?[diouxXeEfFgGcrsa%])', fmt):
        matches.append(m)

    if len(matches) != len(args):
        raise Exception('The numbers of format specifiers and arguments do not match')

    i = len(args) - 1
    for m in reversed(matches):
        f = m.group(1)
        w = m.group(2)
        p = m.group(3) or ''
        c = m.group(4)
        if c == 's' and w:
            w = str(int(w) - wide_count(args[i]))
            fmt = ''.join((fmt[:m.start()], '%', f, w, p, c, fmt[m.end():]))
        i -= 1
    return fmt % args

def printf(fmt, *args):
    '''
    Prints the formatted string of print(fmt % args, end='') similar to
    printf() in C. Note that this function does not add a newline.

    Arguments:
        fmt (str): format string
        *args: arguments for the format string

    Returns:
        None
    '''
    print(f(fmt, *args), end='')
