#!/usr/bin/env python
#-*- coding:utf-8 -*-

import aterm
import sys

import simplify

"""
add "self." to the right places ...

not ready yet ...
"""

DEBUG = False
DECORATE = False

def imported_names(ast):
    res = ["System","Math"]
    for n in ast.findall("TypeImportDec"):
        assert n[0].name == "TypeName"
        assert n[0][1].name == "Id"
        res.append(n[0][1][0])
    return res


def inner_classes(treepos):
    res = []
    for p in treepos.parents():
        if p.name in ['ClassBody']:
            for d in p[0]:
                if d.name in ['ClassDec']:
                  classname = d[0][1][0]
                  res.append(classname)
    return res



def is_static(exp):
    for e in exp.findall("Static"):
        return True
    return False


def method_is_static(exp):
    for e in exp.parents():
        if e.name in ['MethodDec']:
            return is_static(e[0])

def static_classvars(treepos):
    res = []
    for p in treepos.parents():
        if p.name in ['ClassBody']:
            for f in p[0]:
                if f.name in ['FieldDec'] and is_static(f):
                    for v in f.findall("VarDec"):
                        res.append(v[0][0])

    return res


def local_vars(treepos):
    "try to find local vars at treepos"
    res = []
    for n in treepos.walkback():
        if n.name in ['LocalVarDecStm','For']:
            for t in n.findall("VarDec"):
                if t[0].name == 'ArrayVarDecId':
                    res.append(t[0][0][0])
                else:
                    res.append(t[0][0])
        if n.name in ['ForEach','MethodDecHead','ConstrDecHead','Catch']: #TODO interface ?
            for p in n.findall(["Param","VarArityParam"]):
                res.append(p[2][0])

    return res

def fix_names(ast,decorate=DECORATE):
    """
    look for local variables, add __local__ to their name
    add self. to all other variables
    TODO: how to deal with static etc etc
    """
    ast.concat_ids()

    imports = imported_names(ast)
    if DEBUG:
        print "imports:",imports

    interesting = ['FieldDec']

    if decorate:
        # do name decoration for testing purposes
        dec_local = "@l@"
        dec_imported = "@i@"
        dec_innerclass = "@ic@"
    else:
        dec_local = ""
        dec_imported = ""
        dec_innerclass = ""


    for exp in ast.findall(["ExprName","MethodName"]):
        if exp[0].name == "Id":
            if DEBUG:
                print exp
                print "   path:",exp.path()
            local = local_vars(exp)
            if DEBUG:
                print "  locals:",local
            varname = exp[0][0].split('.')[0]
            if varname in local:
                exp[0][0] = dec_local + exp[0][0]
            elif varname in imports:
                exp[0][0] = dec_imported + exp[0][0]
            else:
                if not method_is_static(exp) and varname in static_classvars(exp):
                    exp[0][0] = "self.__class__." + exp[0][0]
                    #print "innerclasses for",exp,inner_classes(exp)
            	else:
                    if not varname[0].isupper():
            	        exp[0][0] = "self." + exp[0][0]
            if 0:
                for n in exp.walkback():
                    print "   ->",n.name
                    if n.name in interesting:
                        print "    ",n

    for exp in ast.findall("NewInstance"):
        #print "checking",exp
        classname = exp[1][0][0][0]
        #print "  classname",classname
        if classname in inner_classes(exp):
            exp[1][0][0][0] = "self." + classname
        else:
            if dec_innerclass is not "":
                exp[1][0][0][0] = dec_innerclass + classname


#or varname[0] in inner_classes(exp):

run = fix_names


if __name__ == '__main__':
    ast = aterm.decode(sys.stdin.read())
    run(ast)
    if not DEBUG:
        print ast
