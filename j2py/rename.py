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
      # "String" : AString("String")
    }
    
    
    for tn in ast.findall("TypeName"):
        if tn[0][0] in ren.keys():
            tn[0][0]=ren[tn[0][0]]
    
    ren = {
      # "class" : "__class__"
    }
 
    kw = "and,del,elif,from,in,is,not,or,print,str,None".split(',')
 
    for id in ast.findall("Id"):
        if id[0] in ren.keys():
            id[0]=AString(ren[id[0]])
        elif id[0] in kw:
            id[0]=AString(id[0]+'_')
            
  

def run(ast):
    rename_ids(ast)
       
if __name__ == '__main__':
    ast = decode(sys.stdin.read())
    run(ast)
    if not DEBUG:
        print ast


