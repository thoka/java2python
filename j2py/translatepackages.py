#!/usr/bin/env python
#-*- coding:utf-8 -*-

import aterm
import sys
import yaml
import os


from simplify import simplify_names

"""
rename packages
"""

DEBUG = False

yamlpath = os.path.join(os.path.dirname(__file__), "translatepackages.yaml")
conversions = yaml.load(open(yamlpath))

def translate_packages(ast):
    for p in ast.findall("TypeImportDec"):
        if DEBUG:
            print p
        if len(p)==1 and p[0][0].name=="Id":
            pkg = p[0][0][0]
            module = p[0][1][0]
            fname = "%s.%s" % (pkg,module) 
            if DEBUG:
                print pkg
            for m,r in conversions.iteritems():
                if pkg.startswith(m):
                    p[0][0].replace(aterm.decode('Id("%s%s")' % (r,pkg[len(m):])) )
                    if DEBUG:
                        print pkg,"-->",p[0][0]
                        print " ",p
                if fname == m :
                    p.replace(aterm.decode('Id("from %s import %s")' % (r,module)))
                    
if __name__ == '__main__':

    if DEBUG:
        print "conversions", conversions
    
    ast = aterm.decode(sys.stdin.read())
    simplify_names(ast)
    translate_packages(ast)
    if not DEBUG:
        print ast


