#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys

"""
runs the main method from a converted java class 
"""

class Dummy(object):
    pass

System = Dummy()
System.out = Dummy()

def println(*args):
    print "".join([ str(i) for i in args])
    
System.out.println = println

def run_class(fname):
    import imp
    M = imp.load_source('',fname)
    M.System = System
    mname = dir(M)[0]
    getattr(M,mname).main(sys.argv)
    
if __name__ == '__main__':
    if len(sys.argv)>1:
        run_class(sys.argv[1])



