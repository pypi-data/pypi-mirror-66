#!/usr/bin/env python

"""
################################################################################
#                                                                              #
# hualang                                                                      #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program makes a Markdown table of media at the working directory.       #
#                                                                              #
# copyright (C) 2020 Will Breaden Madden, wbm@protonmail.ch                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################
"""

name        = "hualang"
__version__ = "2020-04-25T1618Z"

import glob
import re

def files_list(extensions=['*'], directory='.'):
    return [f'{directory}/{f}' for f_ in [glob.glob(g) for g in extensions] for f in f_]

def natural_sort(list_object):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanumeric_key = lambda key: [convert(text) for text in re.split('([0-9]+)', key)]
    return sorted(list_object, key=alphanumeric_key)

def table_Markdown(files, mitigate_whitespace_in_filepath=True, columns=2):
    if mitigate_whitespace_in_filepath:
        files = [f.replace(' ', '&#32;').replace('\t', '&#32;') for f in files]
    if columns == 2:
        if len(files[1::2]) != len(files[::2]):
            files.append('')
        table = '|||\n|---|---|'
        for column_1, column_2 in zip(files[::2], files[1::2]):
            table += f'\n|![]({column_1})|![]({column_2})|'
    return table

def table_Markdown_to_file(filepath='gallery.md', mitigate_whitespace_in_filepath=True, columns=2):
    table = table_Markdown(natural_sort(files_list(extensions=['*.gif', '*.JPEG', '*.jpeg', '*.jpg', '*.JPG', '*.png', '*.PNG', '*.webp', '*.WEBP'])))
    print(table, file=open(filepath, 'w'))
