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
    i = ATerm("Id")
    i.append(AString(code))
    return i

 
def add_init(ast):
    """
    add __init__ to any class in ast
    
    add import of j2py
    """

    imp = decode('Id("from java import System")')
    ast[1].insert(0,imp)

    imp = decode('Id("import java")')
    ast[1].insert(0,imp)
    
    # fix inits for int
    for fd in ast.findall("FieldDec"):
        if fd[1].name in ["Char","Int","Short","Long","Byte","Double","Float"]:
            for vd in fd.findall("VarDec"):
                if len(vd)==1:
                    vd.append(decode('Lit(Deci("0"))'))
        if fd[1].name in ["Boolean"]:
            for vd in fd.findall("VarDec"):
                if len(vd)==1:
                    vd.append(decode('Id("False")'))
        if fd[1].name in ["String"]:
            for vd in fd.findall("VarDec"):
                if len(vd)==1:
                    vd.append(decode('Id("\\"\\"")'))
                       
    for c in ast.findall("ClassDec"):
        body_code = c.findfirst("ClassBody")[0]

        i = make_init()
        block = i[1][0]
        
        for n in body_code:
            if n.name == "FieldDec":
                for v in n.findall("VarDec"):
                    v=v.copy()
                    v[0][0] = AString("self.%s" % v[0][0])
                    block.append(v)
                    if DEBUG:
                        print n
        
        block.append(verbatim("java.dispatch_init(self,*a,**kw)"))
        
        i[0][0].append(ATerm("Id",[AString("@java.init")])) 
        body_code.insert(0,i)
        i.up = body_code ## TODO: this should not be neccesary
        

def add_typed(ast):
    #print "add typed"
    for c in ast.findall("ClassBody"):
        # iterate all definitions in class
        for i in c[0]:
            if i.name == "MethodDec":
                mdh = i[0]
                params = mdh[4]
                if len(params)>0:
                    typed = decode("Typed([])")
                    for param in params:
                        typed[0].append(param[1])
                    if DEBUG:
                        print "params:",params
                        print " -> typed:",typed
                    #print mdh
                    mdh[0].append(typed)
    

if __name__ == '__main__':
    ast = decode(sys.stdin.read())
    add_typed(ast)
    add_init(ast)
    if not DEBUG:
        print ast


