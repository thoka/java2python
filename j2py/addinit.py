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
    [],
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
    i = ATerm("Id",[code])
    #i.append(AString(code))
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
        
        i[0][0].append(ATerm("Id",[AString("@java.init")])) 
        body_code.insert(0,i)
        i.up = body_code ## TODO: this should not be neccesary
        

skipmods=["Public"]
def fix_mods(ast):
    for c in ast.findall("ClassBody"):
        # iterate all definitions in class
        for i in c[0]:
            if i.name in ["MethodDec","ConstrDec"]:
                mdh = i[0]
                mods = mdh[0]
                newmods = AList()
                for m in mods:
                    #print m
                    if m.name not in skipmods:
                       newmods.append(m)
                mdh[0] = newmods


def add_typed(ast):
    #print "add typed"
    for c in ast.findall("ClassBody"):
        # iterate all definitions in class
        for i in c[0]:
            if i.name in ["MethodDec","ConstrDec"]:
                mdh = i[0]
                if i.name == "MethodDec":
                    params = mdh[4]
                else:
                    params = mdh[3]
                if len(params)>0 or i.name=="ConstrDec":
                    typed = decode("Typed([])")
                    for param in params:
                        typed[0].append(param[1])
                    if DEBUG:
                        print "params:",params
                        print " -> typed:",typed
                    #print mdh
                    mdh[0].append(typed)


def decorate_constructor(ast):
    for c in ast.findall("ClassBody"):
        for i in c[0]:
            if i.name in ["ConstrDec"]:
                mdh = i[0]
                cdec = ATerm("Id",["@__init__.register"])
                mdh[0].append(cdec)

def remove_FieldDec(ast):
    for f in ast.findall("FieldDec"):
        f.up.remove(f)
        

def run(ast):
    fix_mods(ast)
    decorate_constructor(ast)
    add_typed(ast)
    add_init(ast)
    remove_FieldDec(ast)

if __name__ == '__main__':
    ast = decode(sys.stdin.read())
    run(ast)
    if not DEBUG:
        print ast
