# how to implemtent static class variables in python ?
class A(object):
    a = 0
    
    def __init__(self):
        print "init a"
        A.a += 1
        
    @classmethod
    def test(self):
        print "A.a",A.a

class B(A):
    b = 0
    
    def __init__(self):
        A.__init__(self)
        print "init b"
        B.b += 1
    
    @classmethod    
    def test(self):
        A.test()
        print "B.b",B.b
        
A.test()
A()
A.test()
B.test()
B()
A.test()
B.test()


