from inspect import isfunction

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
 

def implements(*interfaces):
    def helper(klass):
        klass._interfaces = interfaces
        return klass
        
    return helper
        
def extends(*interfaces):
    def helper(klass):
        klass._extends = interfaces
        return klass
        
    return helper
    


