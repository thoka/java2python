#!/usr/bin/env python
#-*- coding:utf-8 -*-

import aterm

"""
replaces Id's Lit's etc with their content

ast.Something[0][0][0] will then be accessed as ast.Something
"""

@aterm.transformation
def pythonize(ast):

    for e in ast.findall(["Id","Lit"]):
        e.replace(e[0])
    return

    for e in ast.findall(["Deci"]):
        e.replace(int(e[0]))
    for e in ast.findall(["String"]):
        #print e,e[0][0][0]
        e.replace(e[0][0][0])

    return ast
