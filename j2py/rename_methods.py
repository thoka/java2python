#!/usr/bin/env python
#-*- coding:utf-8 -*-

from aterm import *
import sys

"""
TODO write docstring
"""

DEBUG = False
 
 
def rename_methods(ast):
    
    ren = {
        "length" : "__len__"
      , "substring" : "__slice__"            
    }    

    #TODO check also for type
    for id in ast.findall("Id"):
        if id.up.name in ["Method"]:
            if id[0] in ren.keys():
                id[0]=ren[id[0]]    
  
def run(ast):
    rename_methods(ast)
       
if __name__ == '__main__':
    ast = decode(sys.stdin.read())
    run(ast)
    if not DEBUG:
        print ast


