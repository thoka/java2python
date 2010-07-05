#!/usr/bin/env python
#-*- coding:utf-8 -*-

import aterm
import sys


import rename 
from fixnames import fix_names
from translatepackages import translate_packages
import fixstradd
import addinit
from fixcomments import convert_comments
from fixenum import fix_enum
import fix_values
import rename_methods
                
if __name__ == '__main__':
    ast = aterm.decode(sys.stdin.read())
    rename.run(ast)
    fix_values.run(ast)
    convert_comments(ast)
    fix_names(ast)
    rename_methods.run(ast)
    translate_packages(ast)
    fixstradd.run(ast)
 
    addinit.run(ast)
    fix_enum(ast)
    print ast


