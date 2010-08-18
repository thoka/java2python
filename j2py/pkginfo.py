#!/usr/bin/env python
#-*- coding:utf-8 -*-

import aterm
import simplify, pythonize
import sys, os.path
from config import logger

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

VERSION = "0.1.21 (%s)" % yaml.__name__
PKGDATA = 'pkginfo.yaml'

if DEBUG:
    from random import randint
    VERSION += str(randint(0,1000))

TODO = """
docstring from package.html
"""

logger.debug("starting pkginfo")

def decorators(decs):
    """
    makes nice list of decorators out of java ast dec list decs

    [Public()] -> ['public']
    """

    res = []
    for d in decs:
        d = str(d)
        if d.endswith("()"):
            d = d[:-2].lower()
        res.append(d)
    return res


class Java_info(object):
    def is_public(self):
        return 'public' in self.decorators

    def __str__(self):
        return self.name

class Java_Class(Java_info):
    def __init__(self,classdec):
        """
        input:
            - classdec: java ast aterm for this class
        stores following info about class:
            .name classname
            .decorators : ["public","static",...]
        """

        self.name = str(classdec.ClassDecHead[1])
        logger.debug("Java_Class.__init__ %s",self.name)
        #logger.debug(pp_aterm(classdec))
        self.decorators = decorators(classdec.ClassDecHead[0])

        #logger.debug(self.decorators)


class Java_Interface(Java_info):
    def __init__(self,interfacedec):
        self.name = str(interfacedec.InterfaceDecHead[1])
        logger.debug("Java_Interface.__init__ %s",self.name)
        self.decorators = decorators(interfacedec.InterfaceDecHead[0])


class File_Info:

    def __init__(self,fname,srcdir='.'):

        self.fname = fname
        self.srcdir = srcdir

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

        self.imports = []
        for i in cu[1]:
            if i.name == "TypeImportOnDemandDec":
                self.imports.append( "%s.*" % ".".join(i.PackageName[0]) )
            else:
                self.imports.append( "%s.%s" % ( str(i.TypeName[0]), str(i.TypeName[1]) ) )

        #self.used_types = [str(n) for n in set(t[0] for t in cu[2].findall('TypeName') )]


    def __str__(self):
        return "\n".join(["%s: %s" % (n, getattr(self,n)) for n in dir(self) if n[0] != "_" ])

import os.path


from collections import defaultdict


class PackageInfo:
    def __init__(self,basedir,pkg):
        self.basedir = basedir
        self.pkg = pkg
        self.dirname = self.pkg2dir(basedir,pkg)
        self.package = None
        self.files = []

        self._classes = {}
        self._interfaces = {}

        #self.sources = {}
        self.errors = []
        self.pkginfo_version = VERSION
        self.doc = ""
        self.read_dir()

    def add(self,info):

        if not self.package:
            self.package = info.package
        elif self.package != info.package: raise RuntimeError("PackageInfo: wrong package")

        self.files.append(info)

        for c in info.classes:
            self._classes[str(c)] = info
        for i in info.interfaces:
            self._interfaces[str(i)] = info

        #self.sources[info.fname]=info

    def __str__(self):
        res = "package %s:\n c:%s\n i:%s" % (
            self.package,
            ",".join(self.classes.keys()),
            ",".join(self.interfaces.keys())
        )
        return res

    def read_dir(self):
        logger.debug("regenerating pkginfo for %s",self.dirname)
        for n in os.listdir(self.dirname):
            fn = os.path.join(self.dirname,n)
            if n.endswith(".java"):
                logger.debug("parsing %s/%s ...",self.dirname,n)
                #try:
                if True:
                    info = File_Info(n,srcdir=self.dirname)
                    self.add(info)
                #except Exception,e:
                #    logger.warning("class info generation failed for %s: %s",n,e)
                #    self.errors.append([n,str(e)])
            elif n == "package.html":
                from BeautifulSoup import BeautifulSoup

                doc = BeautifulSoup(open(fn).read())
                self.doc = doc.body.renderContents()
            else:
                print "skipping",n


    def save(self):
        logger.debug("saving pkginfo ...")
        fn = os.path.join(self.dirname,PKGDATA)
        f = open(fn,"w")
        yaml.dump(self,f,style="plain") # possible styles: 1quote,2quote,fold,literal,plain
        f.close()


    #todo: add cache

    @classmethod
    def pkg2dir(self,basedir,pkg):
        #if pkg is allready a dirname, return it
        if pkg.find(os.path.sep)>=0: return pkg

        dirname = pkg
        if dirname.find('.')>0:
            dirname = dirname.replace(".",os.path.sep)

        return os.path.join(basedir,dirname)


    @classmethod
    def load(self,basedir,pkg,generate_allways=False):
        """
        loads or generates a pkginfo for java package pkg src, located
        in basedir

        pkg can also be a path to directory containing the pkg sources
        """

        dirname = self.pkg2dir(basedir,pkg)
        fn = os.path.join(dirname,PKGDATA)

        if not generate_allways and os.path.isfile(fn):
            try:
                p = yaml.load(open(fn))
                version = getattr(p,'pkginfo_version',None)
                #regenerate, if version mismatch with stored info
                if  version == VERSION: return p
                logger.debug("pkginfo: version missmatch %s,%s",VERSION,version)
                return self.create(basedir,pkg)
            except Exception,e:
                logger.warning("exception during pkginfo load: %s",e)

        p = PackageInfo(basedir,pkg)
        p.save()
        return p

    @classmethod
    def create(self,basedir,dirname):
        return self.load(basedir,dirname,generate_allways=True)


    def all_classes(self):
        "iterator over all classes defined in this package"
        for ci in self.files:
            for c in ci.classes: yield c

    def public_classes(self):
        for c in self.all_classes():
            if c.is_public(): yield c

    def all_interfaces(self):
        "iterator over all interfaces defined in this package"
        for ci in self.files:
            for i in ci.interfaces: yield i

    def public_interfaces(self):
        for i in self.all_interfaces():
            if True or i.is_public(): yield i



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
