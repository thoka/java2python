#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
from os.path import basename


"""
runs the main method from a converted java class 
"""

def run_class(fname):
    import imp
    M = imp.load_source('',fname)

    #M.System = System
    #M._dispatch_init = _dispatch_init

    classname = basename(fname)[:-3]
    c = getattr(M,classname)
    
    m = None
    try:
        m = c.main
    except:
        pass 
    if m is not None:
        m(sys.argv)
    
    #mname = dir(M)[0]
    #getattr(M,mname).main(sys.argv)
    
if __name__ == '__main__':
    if len(sys.argv)>1:
        run_class(sys.argv[1])
    



