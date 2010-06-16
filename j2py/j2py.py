#!/usr/bin/env python
#-*- coding:utf-8 -*-

import aterm
import sys

from fixnames import fix_names
from translatepackages import translate_packages
from fixstradd import fix_str_add
from addinit import add_init
from fixcomments import convert_comments
                
if __name__ == '__main__':
    ast = aterm.decode(sys.stdin.read())
    convert_comments(ast)
    fix_names(ast)
    translate_packages(ast)
    fix_str_add(ast)
    add_init(ast)
    print ast


