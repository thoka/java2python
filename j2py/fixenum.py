#!/usr/bin/env python
#-*- coding:utf-8 -*-

from aterm import *
import sys

"""
TODO
"""

DEBUG = False

def make_init():
    return decode(init)
    
def verbatim(code):
    #v = ATerm("Verbatim")
    i = ATerm("Id")
    #v.append(i)
    i.append(AString(code))
    
    return i
     
def fix_enum(ast):
    """
    add __init__ to any class in ast
    """
    
def run(ast):
    fix_enum(ast)    
    
if __name__ == '__main__':
    ast = decode(sys.stdin.read())
    run(ast)
    if not DEBUG:
        print ast


