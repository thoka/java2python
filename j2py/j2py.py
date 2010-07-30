#!/usr/bin/env python
#-*- coding:utf-8 -*-

import aterm
import sys

import rename
import fixnames
import translatepackages
import fixstradd
import addinit
import fixcomments
import fixenum
import fix_values
import rename_methods

def run(ast):
    rename.run(ast)
    fix_values.run(ast)
    fixnames.run(ast)
    rename_methods.run(ast)
    translatepackages.run(ast)
    fixstradd.run(ast)
    addinit.run(ast)
    fixenum.run(ast)
    fixcomments.run(ast) #run at least after addinit, to have docstrings in first position

if __name__ == '__main__':
    ast = aterm.decode(sys.stdin.read())
    run(ast)
    print ast
