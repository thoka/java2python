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
import fix_expressions


def run(ast):
    rename.run(ast)
    fix_values.run(ast)
    fix_expressions.run(ast)
    fixnames.run(ast)
    rename_methods.run(ast)
    translatepackages.run(ast)
    fixstradd.run(ast)
    addinit.run(ast)
    fixenum.run(ast)
    fixcomments.run(ast) #run at least after addinit, to have docstrings in first position

if __name__ == '__main__':
    ast = aterm.decode(unicode(sys.stdin.read(),'utf8'))
    run(ast)
    print ast.encode().encode('utf8')
    
