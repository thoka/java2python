#!/usr/bin/env python
#-*- coding:utf-8 -*-

import aterm
import sys
import java_front

DEBUG = False


def strip_java_comment(s):
    """
    returns cleaned list of lines in s
    // /* * etc and empty lines will be removed
    """
    lines = s.split('\n')
    res = []
    skip = ['/**','*/','/']
    for line in lines:
        if line.strip() in skip:
            continue
        line = line.strip('* /')
        res.append(line.strip())

    #delete empty lines at beginning and end
    while len(res)>0 and len(res[0]) == 0: res.pop(0)
    while len(res)>0 and len(res[len(res)-1]) == 0: res.pop()
    return res


def make_docstring(s):
    lines = strip_java_comment(s)
    return aterm.ATerm("DocString",['\n'.join(lines)])


def convert_comment(s,make_docstring=False):
    "convert java comment to python comment or docstring if make_docstring is True"
    res = ['#  ' + l for l in strip_java_comment(s)]
    res = [ aterm.ATerm("S",[l]) for l in res ]

    l = aterm.AList()
    l.extend(res)

    return aterm.ATerm("Verbatim",[l])


def append_annotation(dest,annotation):
    if dest.annotation is None:
        dest.annotation = annotation
    else:
        dest.annotation[0] += annotation[0]


def convert_abstract_method(exp):
    if exp.name != "AbstractMethodDec": raise RuntimeError('AbstractMethodDec expected')

    md = aterm.ATerm('MethodDec')
    exp.replace(md)

    exp.name = 'MethodDecHead'
    md.append(exp)
    md.append(aterm.decode('Block([])'))
    exp[0].insert(0,aterm.ATerm('Abstract'))

    md.annotation = exp.annotation
    exp.annotation = None

    return md

#  java2py-to-box:
#    AbstractMethodDec(mods, type-params, type, Id(n), params, throws)
#      ->
#    box |[ V [
#      H hs=0 [ ~MethodDecHead(mods, type-params, type, Id(n), params, throws) ]
#      "    pass"
#    ] ]|



def convert_comments(ast):
    """
    - converts java comments to python commets
    - moves comments further down in ast tree to change its position
      from before class/method in java to in class/function in pythoin
    """

    make_docstring_for = ['ClassDec','ConstrDec','MethodDec','AbstractMethodDec','AnnoDec','InterfaceDec']

    for exp in ast.walk():
        if isinstance(exp,aterm.ATerm) and exp.annotation is not None:

            p = '/'.join(exp.path()) + '/' + exp.name

            if exp.name in make_docstring_for:
                #try:
                    if exp.name == 'AbstractMethodDec':
                        #print "convert from",exp.pp()
                        exp = convert_abstract_method(exp)
                        #print "to",exp.pp()

                    if exp.name == "MethodDec":
                        if exp[1].name == 'NoMethodBody': exp[1]= aterm.decode('Block([])')

                    #find destination for docstring
                    if exp.name == 'ClassDec':
                        dest = exp.ClassBody[0]
                    elif exp.name == "ConstrDec":
                        dest = exp.ConstrBody[1]
                    elif exp.name == "AnnoDec" or exp.name == "InterfaceDec":
                        dest = exp[1]
                    else:
                        dest = exp.Block[0]

                    docstring = make_docstring(exp.annotation[1])
                    exp.annotation = None
                    dest.insert(0,docstring)
                #except Exception,e:
                #    print "unable to create docstring for", java_front.pp_aterm(exp)
                #    print e
            else:
                exp.annotation[1] = convert_comment(exp.annotation[1])

    # move comments out of inner constructs
    not_wanted = ["Case","[]","()"]
    for exp in ast.walk():
        if isinstance(exp,aterm.ATerm):
            if exp.annotation is not None:
                if DEBUG:
                    print exp.name, exp.path()
                if exp.name in not_wanted:
                    for dest in exp.parents():
                        if not dest.name in not_wanted:
                            break
                    append_annotation(dest,exp.annotation)
                    exp.annotation = None


run = convert_comments

if __name__ == '__main__':
    ast = aterm.decode(sys.stdin.read())
    run(ast)
    print ast
