#!/usr/bin/env python
#-*- coding:utf-8 -*-

from aterm import *
import sys

"""
TODO
"""

DEBUG = False

def fix_values(ast):
    """
    0.3f -> 0.3 etc
    """
    for v in ast.findall(["Float","Deci"]):
        #print v
        if len(v)>0 and not v[0][-1:] in "01234566789":
            v[0] = AString(v[0][0:-1])
            

def run(ast):
    fix_values(ast)
                
if __name__ == '__main__':
    ast = decode(sys.stdin.read())
    run(ast)
    if not DEBUG:
        print ast


