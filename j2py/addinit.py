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


class_init = """
MethodDec(
  MethodDecHead(
    [Static()],
    None,
    Void,
    Id("class_init"),
    [],
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


def add_decorator(dec,mdec):
    mdec[0][0].insert(0,ATerm("Id",["@"+dec]))

def add_init(ast):
    """
    add __init__ to any class in ast
    add import of j2py
    add import of System,Object
    """

    imp = decode('Id("from java import *")')
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
        """
        create init, decoreate overloaded methods
        """

        #insert Object as base class, if none exists
        base_class = c[0][3]
        if base_class.name == "None":
            c[0][3] = ATerm("Id",["Object"])

        body_code = c.findfirst("ClassBody")[0]

        i = make_init()
        block = i[1][0]

        remove = []
        methods = {}
        overloaded_methods = set()

        cblock = decode("[]")

        use_class_init = False

        for n in body_code:
            if n.name == "StaticInit":
                use_class_init = True
                break

        for n in body_code:
            if n.name == "FieldDec":
                dest = block
                if is_static(n):
                    if use_class_init:
                        dest = cblock
                    else:
                        continue
                for v in n.findall("VarDec"):
                    vc=v.copy()
                    vcn = vc.findfirst("Id")
                    vcn[0] = AString("self.%s" % vcn[0])
                    dest.append(vc)
                    if DEBUG:
                        print n
                remove.append(n)
            elif n.name == "StaticInit":
                for e in n[0][0]:
                    cblock.append(e)
                remove.append(n)
            elif n.name == "MethodDec":
                mname = n[0][3][0]
                if not methods.has_key(mname):
                    methods[mname]=n
                else:
                    if mname not in overloaded_methods:
                        add_decorator("java.overloaded",methods[mname])
                        overloaded_methods.add(mname)
                    add_decorator(mname+".register",n)

        for n in remove:
            body_code.remove(n)


        i[0][0].append(ATerm("Id",[AString("@java.init")]))
        body_code.insert(0,i)

        if len(cblock)>0:
            cinit = decode(class_init)
            cinit[1][0]=cblock
            body_code.insert(0,cinit)
            c[0][0].append(ATerm("Id",["@java.use_class_init"]))

skipmods=[]

def filtered_mods(mods):
    newmods = AList()
    for m in mods:
        #print m
        if m.name not in skipmods:
           newmods.append(m)
    return newmods

def fix_mods(ast):
    for c in ast.findall(["ClassBody","EnumBodyDecs"]):
        # iterate all definitions in class
        for i in c[0]:
            if i.name in ["MethodDec","ConstrDec","InterfaceDec","AbstractMethodDec"]:
                mdh = i[0]
                mdh[0] = filtered_mods(mdh[0])


    #interfaces ...
    for idec in ast.findall("InterfaceDec"):
        for i in idec[1]:
            if i.name in ["AbstractMethodDec"]:
                i[0] = filtered_mods(i[0])
        idec[0][0].append(ATerm("Id",["@java.interface"]))

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


def fix_super(ast):
    """
    in java super is called by default
    so add it to python constructor as default too
    """
    for c in ast.findall("ClassDec"):
        # has bases classes ?
        bases = c[0][3]
        if not bases.name == "None":
            for i in c[1][0]:
                if i.name in ["ConstrDec"]:
                    if  i[1][0].name == "None":
                        i[1][0] = decode("Some(SuperConstrInv(None(), []))")

def decorate_inner_classes(ast):
    for c in ast.findall("ClassDec"):
        parents = [ p.name for p in c.parents() ]
        #print c.name,':',parents
        if "ClassDec" in parents:
            c[0][0].append ( ATerm("Id",["@java.innerclass"]) )


def is_static(v):
    return len([i for i in v.findall("Static")]) > 0

def remove_FieldDec(ast):
    #should not be nessesary, since add_init does removal too
    remove = []
    for f in ast.findall("FieldDec"):
        if is_static(f):
            continue
        remove.append(f)
    for f in remove:
        f.up.remove(f)

def run(ast):
    fix_super(ast)
    fix_mods(ast)
    decorate_constructor(ast)
    add_typed(ast)
    decorate_inner_classes(ast)
    add_init(ast)
    remove_FieldDec(ast)

if __name__ == '__main__':
    ast = decode(sys.stdin.read())
    run(ast)
    if not DEBUG:
        print ast
