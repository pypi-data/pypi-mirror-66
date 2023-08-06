#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import setuptools

def main():
    setuptools.setup(
        name             = 'hualang',
        version          = '2020.04.25.1618',
        description      = 'make a Markdown table of images at the working directory',
        long_description = long_description(),
        url              = 'https://github.com/wdbm/hualang',
        author           = 'Will Breaden Madden',
        author_email     = 'wbm@protonmail.ch',
        license          = 'GPLv3',
        packages         = setuptools.find_packages(),
        entry_points     = {
                           'console_scripts': ('hualang_table_Markdown_to_file = hualang.__init__:table_Markdown_to_file')
                           },
        zip_safe         = False
    )

def long_description(filename='README.md'):
    if os.path.isfile(os.path.expandvars(filename)):
      try:
          import pypandoc
          long_description = pypandoc.convert_file(filename, 'rst')
      except ImportError:
          long_description = open(filename).read()
    else:
        long_description = ''
    return long_description

if __name__ == '__main__':
    main()
