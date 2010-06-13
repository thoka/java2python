#!/usr/bin/env python
#-*- coding:utf-8 -*-


import aterm
import sys

import itertools


"""
simplify names

TODO: more doc
"""

DEBUG = False

def simplify_names(ast):
    "replaces AmbNames by Ids" 
    for exp in itertools.chain(aterm.reverse(ast.findall("AmbName")),aterm.reverse(ast.findall("PackageOrTypeName"))):
        if len(exp)==1:
            exp.replace(exp[0])
        elif len(exp)==2:
            if exp[0].name == "Id" and exp[1].name == "Id":
                exp.replace(aterm.decode('Id("%s.%s")' % (exp[0][0],exp[1][0]) ))
 
                
if __name__ == '__main__':
    ast = aterm.decode(sys.stdin.read())
    simplify_names(ast)
    if not DEBUG:
        print ast


