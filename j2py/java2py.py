#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pkginfo
import j2py

import os.path

from translatepackages import rename_pkg
import java_front
from config import config

DEBUG = True
save_intermediates = DEBUG


def package2py(basedir,pkg,outbase):
    """
    translates all java src in pkg to python,
    writes py src into outbase/pkg
    """

    #figure out output dir
    outpkg = rename_pkg(pkg)
    print "outpkg",outpkg


    pkgdir = os.path.join(basedir,pkg.replace(".",os.path.sep))
    outdir = os.path.join(outbase,outpkg.replace(".",os.path.sep))
    if not os.path.isdir(outdir): os.makedirs(outdir)

    print "pkgdir",pkgdir
    print "outdir",outdir

    pi = pkginfo.PackageInfo.load(basedir,pkg)

    #make __init__.py
    of = open(os.path.join(outdir,"__init__.py"),"w")
    of.write('''#-*- coding:utf-8 -*-\n"""%s"""''' % pi.doc)
    of.close()



    for n in os.listdir(pkgdir):
        if n.endswith(".java"):
            print "translating",n

            ast = java_front.parse_java(os.path.join(pkgdir,n))

            if save_intermediates:
                open(os.path.join(outdir,n+".aterm"),"w").write(java_front.pp_aterm(ast))

            j2py.run(ast)

            #todo: add package imports

            if save_intermediates:
                open(os.path.join(outdir,n+".j2py.aterm"),"w").write(java_front.pp_aterm(ast))

            py_ast = java_front.java2py(ast)

            if save_intermediates:
                open(os.path.join(outdir,n+".box"),"w").write(java_front.pp_aterm(py_ast))

            py = java_front.abox2text(py_ast)

            py = py.split("\n")


            #skip
            skip = config['skip']

            def keep(l):
                ls = l.strip()
                if ls in skip: return False
                for s in skip:
                    if ls.startswith(s): return False
                return True

            res = [ l for l in filter(keep,py) ]

            py = "\n".join(res)

            pyfn = n.replace('.java','.py')
            open(os.path.join(outdir,pyfn),'w').write(py)

if __name__ == '__main__':
    basedir = '/home/toka/dv2/google-web-toolkit/user/src/'
    pkg = 'com.google.gwt.user.client'
    outbase = '/home/toka/dv2/google-web-toolkit/user/py/'

    package2py(basedir,pkg,outbase)
