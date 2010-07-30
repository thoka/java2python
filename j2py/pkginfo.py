#!/usr/bin/env python
#-*- coding:utf-8 -*-

import aterm
import simplify
import sys
import os.path
import pythonize

from java_front import parse_java,pp_aterm

try:
    import syck as yaml
except:
    import yaml

"""
Provides information about a package

pi = PackageInfo.load(basedir,pkg)

"""

DEBUG = False

VERSION = "0.1.17 (%s)" % yaml.__name__
PKGDATA = 'pkginfo.yaml'

if DEBUG:
    from random import randint
    VERSION += str(randint(0,1000))

TODO = """
docstring from package.html
"""

class Java_Class:
    def __init__(self,classdec):
        self.name = str(classdec.ClassDecHead[1])
    def __str__(self):
        return self.name

class Java_Interface:
    def __init__(self,interfacedec):
        self.name = str(interfacedec.InterfaceDecHead[1])
    def __str__(self):
        return self.name

class class_info:

    def __init__(self,fname,srcdir='.'):

        self.fname = fname

        ast = parse_java(os.path.join(srcdir,fname))
        ast.concat_ids().pythonize()

        cu = ast.CompilationUnit

        self.package = None
        pn = ast.PackageDec.PackageName
        if pn:
            self.package = ".".join(pn[0])

        self.classes = []
        self.interfaces = []

        for d in cu[2]:
            if d.name == 'ClassDec':
                self.classes.append(Java_Class(d))
            if d.name == 'InterfaceDec':
                self.interfaces.append(Java_Interface(d))
                # print pp_aterm(d)

        self.imports = [ [ str(i.TypeName[1]) ,str(i.TypeName[0]) ] for i in cu[1] ]
        #self.used_types = [str(n) for n in set(t[0] for t in cu[2].findall('TypeName') )]


    def __str__(self):
        return "\n".join(["%s: %s" % (n, getattr(self,n)) for n in dir(self) if n[0] != "_" ])

import os.path


from collections import defaultdict


class PackageInfo:
    def __init__(self,basedir,dirname):
        self.basedir = basedir
        self.dirname = dirname
        self.package = None
        self.classes = {}
        self.interfaces = {}
        #self.sources = {}
        self.errors = []
        self.pkginfo_version = VERSION
        self.doc = ""
        self.read_dir()

    def add(self,info):
        if not self.package:
            self.package = info.package
        elif self.package != info.package: raise RuntimeError("PackageInfo: wrong package")
        for c in info.classes:
            self.classes[str(c)] = info
        for i in info.interfaces:
            self.interfaces[str(i)] = info
        #self.sources[info.fname]=info

    def __str__(self):
        res = "package %s:\n c:%s\n i:%s" % (
            self.package,
            ",".join(self.classes.keys()),
            ",".join(self.interfaces.keys())
        )
        return res

    def read_dir(self):
        for n in os.listdir(self.dirname):
            fn = os.path.join(self.dirname,n)
            if n.endswith(".java"):
                print "parsing",n,"in",self.dirname,"..."
                try:
                    info = class_info(n,srcdir=self.dirname)
                    self.add(info)
                except Exception,e:
                    print "  failed:",e
                    self.errors.append([n,str(e)])
            elif n == "package.html":
                from BeautifulSoup import BeautifulSoup

                doc = BeautifulSoup(open(fn).read())
                self.doc = doc.body.renderContents()
            else:
                print "skipping",n


    def save(self):
        print "save ..."
        fn = os.path.join(self.dirname,PKGDATA)
        yaml.dump(self,open(fn,"w"),style="plain") # possible styles: 1quote,2quote,fold,literal,plain


    #320 012 34 56
    #051 576 89 07


    #todo: add cache

    @classmethod
    def load(self,basedir,pkg,generate_allways=False):
        """
        loads or generates a pkginfo for package pkg src, located
        in basedir

        pkg can also be a path to directory containing the pkg sources
        """

        dirname = pkg
        if dirname.find('.')>0:
            dirname = dirname.replace(".",os.path.sep)
            dirname = os.path.join(basedir,dirname)

        fn = os.path.join(dirname,PKGDATA)
        if not generate_allways and os.path.isfile(fn):
            try:
                p = yaml.load(open(fn))
                if getattr(p,'pkginfo_version',None) == VERSION:
                    return p
                return self.create(basedir,dirname)
            except: pass

        p = PackageInfo(basedir,dirname)
        p.save()
        return p

    @classmethod
    def create(self,basedir,dirname):
        return self.load(basedir,dirname,generate_allways=True)


def create_pkg(basedir,dirname,fnames):
    if dirname.find("/.svn") >=0: return
    print "create pkg",basedir,dirname
    p = PackageInfo.create(basedir,dirname)
    print p
    print p.doc
    #print


def create_pkgs(basedir):
    os.path.walk(basedir,create_pkg,basedir)


def main():
    basedir = '/home/toka/dv2/google-web-toolkit/user/src/'

    ## create

    # create_pkgs(dirname)

    p = PackageInfo.load(basedir,'com.google.gwt.user.client')
    print p
    print p.doc

    # print yaml.dump(p)


if __name__ == '__main__':
    sys.exit(main())
