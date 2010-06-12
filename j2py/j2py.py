#!/usr/bin/env python
#-*- coding:utf-8 -*-

import aterm
import sys

from fixcomments import convert_comments
from fixnames import fix_names
from translatepackages import translate_packages
from fixstradd import fix_str_add
                
if __name__ == '__main__':
    ast = aterm.decode(sys.stdin.read())
    convert_comments(ast)
    fix_names(ast)
    translate_packages(ast)
    fix_str_add(ast)
    print ast


