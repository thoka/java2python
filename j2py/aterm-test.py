#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Unittests for aterm.

TODO:
- ATerm.parents()
- ATerm.path()

"""

import unittest

#TODO: is there a better way to do this ?
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aterm import decode, ATerm, ATuple
from itertools import izip,count

class TestDecode(unittest.TestCase):
    def de(self,l,r):
        lval = decode(l)
        self.assertEquals()

    def test_simple(self):
        t = decode('T')
        self.assert_(isinstance(t, ATerm))
        self.assertEquals(t.name, 'T')
        self.assertEquals(len(t), 0)
        t = decode('T()')
        self.assert_(isinstance(t, ATerm))
        self.assertEquals(t.name, 'T')
        self.assertEquals(len(t), 0)
        t = decode('()')
        self.assert_(isinstance(t, ATuple))
        self.assertEquals(t.name, '()')
        self.assertEquals(len(t), 0)


    def test_annotation(self):
        t = decode("T()")
        self.assertEquals(t.annotation, None)
        t = decode("T(){}")
        self.assertEquals(t.annotation, None)
        t = decode("A(B(){C()}){1}")
        self.assert_(isinstance(t, ATerm))
        self.assertEquals(t.annotation, 1)
        self.assertEquals(t[0].annotation.encode(),"C()")


    def test_allatonce(self):
        t = decode('T("", "bla", "bla" , S([ "", "bla", "bla" ] ))')
        self.assert_(isinstance(t, ATerm))
        self.assertEquals(t.name, "T")
        self.assertEquals(len(t), 4)

    def test_strings(self):
        t = decode('T("")')
        self.assert_(isinstance(t, ATerm))
        self.assertEquals(len(t[0]), 0)
        t = decode('T("\\"")')
        self.assert_(isinstance(t, ATerm))
        self.assertEquals(len(t[0]), 1)
        t = decode('T("\\"\\"")')
        self.assert_(isinstance(t, ATerm))
        self.assertEquals(len(t[0]), 2)
        t = decode('T("äö")')
        self.assert_(isinstance(t, ATerm))
        self.assertEquals(len(t[0]), 2)

class TestTree(unittest.TestCase):
    def test_tree(self):
        t = decode('A(B(C()),[])')
        self.assertEquals(t.up, None)
        self.assertEquals(t[0].name, "B")
        self.assertEquals(t[0].up, t)
        self.assertEquals(t[1].up, t)

    def test_walk(self):
        t = decode("A(B(C(),D()))")
        w = ''.join([n.name for n in t.walk()])
        self.assertEquals(w, "ABCD")

    def test_walkback(self):
        t = decode('A(B(),B(C(D(),E())),F())')
        e = t.findfirst('E')
        wb = ''.join([ n.name for n in e.walkback()])
        self.assertEquals(wb,'DCBBA')

    def test_append(self):
        a = ATerm("a")
        b = ATerm("b")
        a.append(b)
        self.assertEquals(a,b.up)

    def test_setitem(self):
        a = ATerm("a",[1])
        b = ATerm("b")
        a[0]=b
        self.assertEquals(a,b.up)

    def test_insert(self):
        a = ATerm("a")
        b = ATerm("b")
        a.insert(0,b)
        self.assertEquals(a,b.up)
        a = ATerm("a",[1])
        b = ATerm("b")
        a.insert(0,b)
        self.assertEquals(a,b.up)



class TestEncode(unittest.TestCase):
    def de(self,src,enc=None):
        d = decode(src)
        if enc is None:
            enc = src
        self.assertEquals(d.encode(),enc)

    def test_decode_encode(self):
        self.de('A','A()')
        self.de('A()')
        self.de('A(){}','A()')
        self.de('A(){1}','A(){1}')
        self.de(u'A("ä")')
        self.de('A("")')
        self.de('A("\\"")')
        self.de('A("b")')
        self.de('A([])')
        self.de('A([B()])')
        self.de('A([B(),C()])')


class TestPos(unittest.TestCase):
    def test_pos(self):
        t = decode('A(B(),C(),D())')
        self.assertEquals(t[0].name, "B")
        self.assertEquals(t[0].pos(), 0)
        self.assertEquals(t[1].name, "C")
        self.assertEquals(t[1].pos(), 1)
        self.assertEquals(t[2].name, "D")
        self.assertEquals(t[2].pos(), 2)

class TestFind(unittest.TestCase):
    def test_find(self):
        t = decode('A(B(C(D())),[])')
        r = [i for i in t.findall('C') ]
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0][0].name,"D")
        r = [i for i in t.findall(['B','C']) ]
        self.assertEquals(len(r), 2)

if __name__ == '__main__':
    unittest.main()
