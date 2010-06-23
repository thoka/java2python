#!/usr/bin/env python
#-*- coding:utf-8 -*-

import aterm
import sys


from renameids import rename_ids
from fixnames import fix_names
from translatepackages import translate_packages
from fixstradd import fix_str_add
import addinit
from fixcomments import convert_comments
from fixenum import fix_enum

import fix_values
                
if __name__ == '__main__':
    ast = aterm.decode(sys.stdin.read())
    rename_ids(ast)
    fix_values.run(ast)
    convert_comments(ast)
    fix_names(ast)
    translate_packages(ast)
    fix_str_add(ast)
 
    addinit.run(ast)
    fix_enum(ast)
    print ast


