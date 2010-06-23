from enum import Enum,enum
from inspect import isfunction

def init(func):
    return func

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

def typed(*sig):
    def add_sig(f):
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
    def __init__(self,f):
        self.registry = {}
        self.init = f 
        
    def __get__(self,obj,typename):
        self.self = obj
        return self
        
    def register_func(self, func, sig):
        key = typeid(sig)
        self.registry[key] = func
        
    def register(self,func):
        self.register_func(func,func._type_sig)
        return self
   
    def __call__(self,*a):
        key = argtypeid(a)
        func = self.registry.get(key,None)
        self.init(self.self,*a)
        if func is not None:
            func(self.self,*a)
        elif key == tuple():
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
        

class override(object):
    def __init__(self,f):
        self.registry = {}
        self.register_func(f,f._type_sig)
        
    def register_func(self, func, sig):
        key = typeid(sig)
        self.registry[key] = func
        
    def override(self,f):
        self.register_func(f,f._type_sig)
        return self
    
    def __call__(self,*a):
        key = argtypeid(a)
        func = self.registry.get(key,None)
        if func is not None:
            return func(self,*a)
        else:
            raise RuntimeError("no function for signature " + str(key))


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
    
_str = str

def str(o):
    if o is None:
        return ""
    else:
        return _str(o)
            
System.out.println = println

#__all__ = "Enum,enum,System,_dispatch_init,init,typed".split(',')


    

