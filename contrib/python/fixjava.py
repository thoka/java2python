#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Fixes issues, which pp-java2py can not handle (yet?)

- Comments


TODO:
- 
 
"""

import aterm
import sys

ast = aterm.decode(sys.stdin.read())

def path(exp):
    "gives a filesystem style path to node exp" 
    res = [ p.name for p in exp.parents() ]
    res.reverse()
    return '/'.join(res)
        
        
def convert_comment(s,make_docstring=False):
    "convert java comment to python comment or docstring if make_docstring is True"
    lines = s.split('\n')
    res = []
    skip = ['/**','*/','/']
    for line in lines:
        if line.strip() in skip:
            continue
        line = line.strip('* /')
        res.append(line)
    while len(res)>0 and len(res[0]) == 0:
        res.pop(0)
    while len(res)>0 and len(res[len(res)-1]) == 0:
        res.pop()
    if not False and make_docstring: #currently not activated, do not know hot to render that correctly
        if len(res)>2:
            res=["    '''"]+["        "+l for l in res]+["        '''"]
        elif len(res)==1:
            res[0]='    ''%s''' % res[0]    
    else:
        res=['# '+l for l in res]        
    return aterm.AString('\n'.join(res))    




for exp in j.findall("AmbName"):
    if len(exp)==1:
        exp.replace(exp[0])
    elif len(exp)==2:
        if exp[0].name == "Id" and exp[1].name == "Id":
            exp.replace(aterm.decode('Id("%s.%s")' % (exp[0][0],exp[1][0]) ))

if 0:
    for exp in j.findall("ExprName"):
        if len(exp) == 2:
            print exp, exp[0].name == "Id" , exp[0][0]


def convert_comments(ast):
    """
    - converts java comments to python commets
    - moves comments further down in ast tree to change its position
      from before class/method in java to in class/function in pythoin 
    """
    
    make_docstring = ['ClassDec','ConstrDec','MethodDec']
    move = []

    for exp in ast.walk():
        if isinstance(exp,aterm.ATerm):
            if exp.annotation is not None:
                # print path(exp),exp.name
                # print "  ",exp
                # print "  ",convert_comment(exp.annotation[1], exp.name in ['ClassDec','ConstrDec','MethodDec'])
                # print

                exp.annotation[1] = convert_comment(exp.annotation[1], exp.name in make_docstring)
                
                if exp.name in make_docstring:
                    move.append(exp)
                    
    for exp in move:
        exp[1].annotation = exp.annotation
        exp.annotation = None
            

convert_comments(ast)

print ast



