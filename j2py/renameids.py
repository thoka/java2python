#!/usr/bin/env python
#-*- coding:utf-8 -*-

from aterm import *
import sys

"""
rename ids, class -> __class__ etc ...
"""

DEBUG = False
 
def rename_ids(ast):
    """
    """
    
    ren = {
      "String" : AString("java.String")
    }
    
    
    for tn in ast.findall("TypeName"):
        if tn[0][0] in ren.keys():
            tn[0][0]=ren[tn[0][0]]
    
    ren = {
      "class" : AString("__class__")
    }

    for id in ast.findall("Id"):
        if id[0] in ren.keys():
            id[0]=ren[id[0]]       
   
if __name__ == '__main__':
    ast = decode(sys.stdin.read())
    rename_ids(ast)
    if not DEBUG:
        print ast


