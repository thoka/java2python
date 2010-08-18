from subprocess import Popen,PIPE

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

import aterm
import os
import sys

"""
makes java front programs accessable from python
"""

FIX_PP_BUG = True

class run_cmd:

    def __init__(self,command,instr=""):
        self.command = command
        p = Popen(command, stdin=PIPE,stderr=PIPE, stdout=PIPE)
        self.res,self.err = p.communicate(instr)
        self.res=unicode(self.res,'utf8')
        self.err=unicode(self.res,'utf8')

    def __str__(self):
        return "%s\n  res=%s\n  err=%s" % (self.command,self.res,self.err)

class ParseError(Exception):
    pass


def parse_java(fname):
    pj = run_cmd(['parse-java','--preserve-comments','-i',fname])

    if len(pj.err)>0:
        raise ParseError('parse-java:'+pj.err)
    return aterm.decode(pj.res)

import string

@aterm.transformation
def fixpp(ast):
    if not FIX_PP_BUG: return ast
    "fix pp-aterm bug (\" isnot escaped inside comments)"
    for exp in ast.walk():
        if isinstance(exp,aterm.ATerm) and exp.annotation is not None:
            c = exp.annotation[1]
            if isinstance(c,str):
                exp.annotation[1] = c.replace("\"","\\\"")
            else:
                for s in c.findall("S"):
                    s[0] = s[0].replace("\"","\\\"")
    return ast

def pp_aterm(s):
    if isinstance(s,aterm.ATerm): s = str(s.copy().fixpp())
    return run_cmd(['pp-aterm'],s).res

@aterm.transformation
def pp(s):
    return pp_aterm(s)

def java2py(s):
    if isinstance(s,aterm.ATerm): s = str(s)
    run = run_cmd([os.path.join(os.path.dirname(__file__), "../tools/java2py")],s)
    if len(run.err)>0: sys.stderr.write(run.err)
    return run.res

def abox2text(s):
    if isinstance(s,aterm.ATerm): s = str(s)
    run = run_cmd(["abox2text","--width","1000"],s)
    if len(run.err)>0: sys.stderr.write(run.err)
    return run.res
