#!/usr/bin/env python
#-*- coding:utf-8 -*-
import aterm
import sys

import itertools

"""
java supports adding of string and integer, for example
python not

therefore, replace str + expr with str + str(expr)
"""

DEBUG = False
        
def is_string(e):
    return (e.name == "Lit" and e[0].name=="String") or e.name == "ToStr"
            

def make_string(e):
    return aterm.decode("ToStr(%s)" % repr(e))

def fix_str_add(ast):
    "replace str + expr with str + str(expr)" 
    for p in aterm.reverse(ast.findall("Plus")):
        if len(p)==2:
            if is_string(p[0]) or is_string(p[1]):
               if not is_string(p[0]):
                    p[0].replace(make_string(p[0]))
               if not is_string(p[1]):
                    p[1].replace(make_string(p[1])) 
                
if __name__ == '__main__':
    ast = aterm.decode(sys.stdin.read())
    fix_str_add(ast)
    if not DEBUG:
        print ast


