#!/usr/bin/env python
#-*- coding:utf-8 -*-

import aterm
import sys

"""
renames java methods to match python methodnames

currently only some string methods will be renamed
"""

DEBUG = False

def has_type(exp,t):
    #TODO: implement typecheck
    return True

@aterm.transformation
def rename_methods(ast):

    ren = {
        "length" : "__len__"
       ,"indexOf" : "find"
       ,"lastIndexOf" : "rfind"
       ,"startsWith" : "startswith"
       ,"endsWith" : "endswith"

    }

    #TODO check also for type

    to_rename = ren.keys()

    for i in ast.findall("Invoke"):
        if i[0].name == "Method" and len(i[0])==1 \
            and i[0][0].name=="MethodName" and len(i[0][0])==2:

            m = i[0][0]
            obj,methodname = m[0][0],m[1][0]

            if has_type(obj,"String"):
                if methodname == "substring":
                    args = m.up.up[1]
                    if len(args)==1: args.append(aterm.ATerm("Id",[""]))
                    sl = aterm.ATerm("Slice",[m[0]])
                    sl.extend(args)
                    #TODO: copy comments
                    m.up.up.replace(sl)
                    continue
                elif methodname == "charAt":
                    arg = m.up.up[1]
                    a = aterm.ATerm("ArrayAccess",[m[0]])
                    a.extend(arg)
                    m.up.up.replace(a)
                    #TODO: copy comments
                    continue

            if methodname in to_rename:
                #print "rename to", ren[methodname]
                m[1][0] = ren[methodname]

        elif i[0].name == "Method" and len(i[0])==3:
            m = i[0]
            obj,methodname = m[0][0],m[2][0]

            if methodname in to_rename:
                #print "rename to", ren[methodname]
                m[2][0] = ren[methodname]

    return ast


@aterm.transformation
def to_slice(ast):
    for i in ast.findall():
        pass
    return ast

def run(ast):
    rename_methods(ast)

if __name__ == '__main__':
    ast = decode(sys.stdin.read())
    run(ast)
    if not DEBUG:
        print ast
