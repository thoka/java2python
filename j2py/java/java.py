from enum import Enum,enum,EnumItem
from inspect import isfunction

"""
java runtime lib for j2py
"""

# DECORATORS

def static(something):
    #print "@static", something,isfunction(something)
    if isfunction(something):
        return classmethod(something)
    else:
        return staticclass(something)

def protected(func):
    return func
    
def volatile(func):
    return func

def final(func):
    return func

def private(func):
    return func

def constructor(func):
    return func
    
def interface(c):
    return c    

def typed(*sig):
    def add_sig(f):
        "typed add_sig",f,sig
        f._type_sig = sig
        return f
    return add_sig            

def typeid(a):    
    if isinstance(a,list) or isinstance(a,tuple):
        return tuple(typeid(i) for i in a)
    elif isinstance(a,type):
        return a
    else:
        return type(a)

def argtypeid(a,d=0):
    if isinstance(a,tuple):
        return tuple(argtypeid(i,d+1) for i in a)
    elif isinstance(a,list):
        return (argtypeid(a[0]),) #TODO: add check, if all types are equal
    else:
        return type(a)

class init(object):

    def __repr__(self):
        if self.klass is None:
            return "<init decorator for %s>" % repr(self.init)
        else:
            return "<init %s>" % self.klass.__name__

    def __init__(self,f):
        #print "@init __init__",self,f
        self.registry = {}
        self.self = None
        self.klass = None
        self.init = f 
        self.inits = None
        
    def __get__(self,obj,klass):
        #print "@init __get__",self,obj,klass
        if obj is not None:
            self.self = obj
            self.klass = klass
        return self
        
    def register_func(self, func, sig):
        #print "@init register_func",self,func,sig
        key = typeid(sig)
        self.registry[key] = func
        
    def register(self,func):
        #print "@init register",self,func
        self.register_func(func,func._type_sig)
        return self


    def _super(self,*a):
        key = argtypeid(a)
        #print "init super",a,"key",key

        for i in reversed(self.inits[:-1]):
            func = i.registry.get(key,None)
            if func is not None:
                #print " call super", func
                func(self.self,*a)
                return
   
    def __call__(self,*a):
        key = argtypeid(a)
        #print "@init __call__",self,a,key
        
        # find constructors for base classes
        if self.inits is None:
            k = self.klass
            inits = []
            while True:
                inits.insert(0,k.__init__)
                #print " .. bases", k.__bases__
                base_found = False
                
                for b in k.__bases__:
                    try:
                        i = b.__init__
                        #print " ...init=",i 
                        if isinstance(b.__init__,init):
                            #print "found one",b
                            k = b
                            base_found = True
                    except:
                        pass
                        #print "no java baseclass",b
                if not base_found: break
            #print " ... inits:",inits
            self.inits = inits
            
        # call __init__ for all java base classes
        for i in self.inits:
            #print " var-init",i.init
            i.init(self.self)

        # find and call __init__(key)
        #inits.reverse()
        
        for i in reversed(self.inits):
            func = i.registry.get(key,None)
            if func is not None:
                #print " constr init", func
                func(self.self,*a)
                return
                
        if key == tuple():
            #print "@init __call__ () not registered"
            pass
        else:
            raise RuntimeError("No constructor found for signature " + str(key))




class innerclass(object):
    def __init__(self,innerclass):
        #print "innerclass init",innerclass
        self.innerclass = innerclass
    
    def __get__(self,obj,typename):
        #print "innerclass get",obj,typename
        self.upperclass = typename
        self.innerclass.upperclass = typename
        return self.innerclass
        
        
class staticclass(object):
    def __init__(self,innerclass):
        #print "staticclass init",innerclass
        self.innerclass = innerclass
    
    def __get__(self,obj,t):
        #print "staticcclass get",obj,t
        self.self = obj
        self.t = t
        return self
        
    def __call__(self,*a):
        #print "staticclass call",a
        return self.innerclass.__get__(None,self.t)
        

class overloaded(object):
    def __init__(self,f):
        #print "overloaded init",f
        self.registry = {}
        try:
            self.register_func(f,f._type_sig)
        except:
            self.register_func(f,tuple())       

    def __get__(self,obj,t):
        #print "overloaded get",obj,t
        self.self = obj
        self.t = t
        return self
        
    def register_func(self, func, sig):
        key = typeid(sig)
        self.registry[key] = func
        
    def register(self,f):
        self.register_func(f,f._type_sig)
        return self
    
    def __call__(self,*a):
        #print "overloaded call",a
        key = argtypeid(a)
        func = self.registry.get(key,None)
        if func is not None:
            return func(self.self,*a)
        else:
            raise RuntimeError("no function for signature " + str(key))

# Objects ...


class Array(list):
    def __getattr__(self,key):
        if key == 'length':
            return len(self)
        raise Exception('key not found') #TODO raise right exception, read docs ...
                            
class Object(object):
    pass


String = "".__class__

System = Object()
System.out = Object()

def println(*args):
    print "".join([ str(i) for i in args])

System.out.println = println
   
# helpers

# ... simulate java in str()

_str = str
def str(o):
    if o is None:
        return ""
    else:
        return _str(o)
        
# >>> operator

def bsr(value, bits):
    """ bsr(value, bits) -> value shifted right by bits

    This function is here because an expression in the original java
    source contained the token '>>>' and/or '>>>=' (bit shift right
    and/or bit shift right assign).  In place of these, the python
    source code below contains calls to this function.

    Copyright 2003 Jeffrey Clement.  See pyrijnadel.py for license and
    original source.
    """
    minint = -2147483648
    if bits == 0:
        return value
    elif bits == 31:
        if value & minint:
            return 1
        else:
            return 0
    elif bits < 0 or bits > 31:
        raise ValueError('bad shift count')
    tmp = (value & 0x7FFFFFFE) // 2**bits
    if (value & minint):
        return (tmp | (0x40000000 // 2**(bits-1)))
    else:
        return tmp        
            
def bsl(value,bits):
    raise NotImplemented
                

# dummy, allows building of parameterized classes                
# TODO
def typechecker(*a):
    return None
                               
