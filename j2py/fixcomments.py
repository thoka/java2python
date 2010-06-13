#!/usr/bin/env python
#-*- coding:utf-8 -*-

import aterm
import sys
        
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
    if make_docstring: 
        if True or len(res)>2:
            res=['    """']+["        "+l for l in res]+['        """']
        elif len(res)==1:
            res[0]='  "%s"' % res[0]    
    else:
        res=['# '+l for l in res]        
    return aterm.AString('\n'.join(res))    

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
                # print exp.path(),exp.name
                # print "  ",exp
                # print "  ",convert_comment(exp.annotation[1], exp.name in ['ClassDec','ConstrDec','MethodDec'])
                # print

                exp.annotation[1] = convert_comment(exp.annotation[1], exp.name in make_docstring)
                
                if exp.name in make_docstring:
                    move.append(exp)
                    
    for exp in move:
        exp[1].annotation = exp.annotation
        exp.annotation = None    
                 
if __name__ == '__main__':
    ast = aterm.decode(sys.stdin.read())
    convert_comments(ast)
    print ast
    



