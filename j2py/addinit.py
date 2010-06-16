#!/usr/bin/env python
#-*- coding:utf-8 -*-

from aterm import *
import sys

"""
add __init__(self)
"""

DEBUG = False

init = """
MethodDec(
  MethodDecHead(
    [Public],
    None,
    Void,
    Id("__init__"),
    [Param([],ClassOrInterfaceType(TypeName(Id("Object")),None),Id("*a, **kw"))],
    None),
  Block([])
)
"""

def make_init():
    return decode(init)
    
def verbatim(code):
    #v = ATerm("Verbatim")
    i = ATerm("Id")
    #v.append(i)
    i.append(AString(code))
    
    return i
    
  
 
def add_init(ast):
    """
    add __init__ to any class in ast
    """
    for c in ast.findall("ClassDec"):
        body_code = c.findfirst("ClassBody")[0]

        i = make_init()
        block = i[1][0]
        
        for n in body_code:
            if n.name == "FieldDec":
                v = n.findfirst("VarDec").copy()
                v[0][0] = AString("self.%s" % v[0][0])
                block.append(v)
                if DEBUG:
                    print n
        
        block.append(verbatim("_dispatch_init(self,*a,**kw)"))
        
        i[0][0].append(ATerm("Decorator",[AString("init")])) 
        body_code.insert(0,i)
        i.up = body_code ## TODO: this should not be neccesary
        
    
if __name__ == '__main__':
    ast = decode(sys.stdin.read())
    add_init(ast)
    if not DEBUG:
        print ast


