#!/usr/bin/env python
#-*- coding:utf-8 -*-

import aterm
import sys
import yaml
import os
from config import config
import simplify

"""
rename packages
"""

DEBUG = False

conversions = config["rename-packages"]

def rename_pkg(pkg,module=None):
    """
    applies configured translations to pkg
    returns translated pkg name
    """

    if module is not None:
        module = "%s.%s" % (pkg,module)

    for m,r in conversions.iteritems():
        if pkg == m or module == m: return r
        if pkg.startswith(m): return r + pkg[len(m):]

    return module


def translate_packages(ast):
    for p in ast.findall("TypeImportDec"):
        if DEBUG:
            print p
        if len(p)==1 and p[0][0].name=="Id":
            pkg = p[0][0][0]
            module = p[0][1][0]
            rpkg = rename_pkg(pkg,module)
            if rpkg != pkg:
                p[0][0].replace(aterm.decode('Id("%s")' % (rpkg)) )
                if DEBUG:
                    print pkg,"-->",p[0][0]
                    print " ",p

run = translate_packages


if __name__ == '__main__':

    if DEBUG:
        print "conversions", conversions

    ast = aterm.decode(sys.stdin.read())
    simplify_names(ast)
    translate_packages(ast)
    if not DEBUG:
        print ast
