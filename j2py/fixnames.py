#!/usr/bin/env python
#-*- coding:utf-8 -*-

import aterm
import sys

from simplify import simplify_names


"""
add "self." to the right places ...

not ready yet ...
"""

DEBUG = False

def imported_names(ast):
    res = ["System","Math"]
    for n in ast.findall("TypeImportDec"):
        assert n[0].name == "TypeName"
        assert n[0][1].name == "Id"
        res.append(n[0][1][0])
    return res    
 
def local_vars(treepos):
    "try to find local vars at treepos"
    res = []
    for n in treepos.walkback():
        if n.name in ['FieldDec','LocalVarDecStm']:
            for t in n.findall("VarDec"):
                res.append(t[0][0])
        if n.name in ['MethodDecHead']:
            for p in n.findall("Param"):
                res.append(p[2][0])
    return res          
 
def fix_names(ast,decorate=False):
    """
    look for local variables, add __local__ to their name
    add self. to all other variables
    TODO: how to deal with static etc etc
    """
    simplify_names(ast)
    
    imports = imported_names(ast)
    if DEBUG:
        print "imports:",imports
     
    interesting = ['FieldDec'] 
    
    if decorate:
        # do name decoration for testing purposes 
        dec_local = "@l@"
        dec_imported = "@i@"
    else:
        dec_local = ""
        dec_imported = ""

    
    if 1:
        for exp in ast.findall(["ExprName","MethodName"]):
            if True or len(exp) == 2:
                if exp[0].name == "Id":
                    if DEBUG: 
                        print exp
                        print "   path:",exp.path()
                    local = local_vars(exp)
                    if DEBUG:
                        print "  locals:",local
                    varname = exp[0][0].split('.')[0]  
                    if varname in local:
                        exp[0][0] =aterm.AString(dec_local + exp[0][0])
                    elif varname in imports:
                        exp[0][0] =aterm.AString(dec_imported + exp[0][0])
                    else:
                        exp[0][0] =aterm.AString("self." + exp[0][0])                    
                    if 0:    
                        for n in exp.walkback():
                            print "   ->",n.name
                            if n.name in interesting:
                                print "    ",n
                                
                        
                        #print exp, exp[0].name == "Id" , exp[0][0]
                

if __name__ == '__main__':
    ast = aterm.decode(sys.stdin.read())
    fix_names(ast)
    if not DEBUG:
        print ast


