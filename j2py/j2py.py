#!/usr/bin/env python
#-*- coding:utf-8 -*-

import aterm
import sys

from renameids import rename_ids
from fixnames import fix_names
from translatepackages import translate_packages
from fixstradd import fix_str_add
from addinit import add_init,add_typed
from fixcomments import convert_comments
from fixenum import fix_enum
                
if __name__ == '__main__':
    ast = aterm.decode(sys.stdin.read())
    rename_ids(ast)
    convert_comments(ast)
    fix_names(ast)
    translate_packages(ast)
    fix_str_add(ast)
    add_typed(ast)
    add_init(ast)
    fix_enum(ast)
    print ast


