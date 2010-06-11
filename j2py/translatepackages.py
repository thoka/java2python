#!/usr/bin/env python
#-*- coding:utf-8 -*-

import aterm
import sys
import yaml

from simplify import simplify_names

"""
rename packages
"""

DEBUG = False

conversions = yaml.load(open("translatepackages.yaml"))

def translate_packages(ast):
    for p in ast.findall("TypeImportDec"):
        if DEBUG:
            print p
        if len(p)==1 and p[0][0].name=="Id":
            pkg = p[0][0][0]
            if DEBUG:
                print pkg
            for m,r in conversions.iteritems():
                if pkg.startswith(m):
                    p[0][0].replace(aterm.decode('Id("%s%s")' % (r,pkg[len(m):])) )
                    if DEBUG:
                        print pkg,"-->",p[0][0]
                        print " ",p
               
if __name__ == '__main__':

    if DEBUG:
        print "conversions", conversions
    
    ast = aterm.decode(sys.stdin.read())
    simplify_names(ast)
    translate_packages(ast)
    if not DEBUG:
        print ast


