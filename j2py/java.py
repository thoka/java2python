from enum import Enum,enum

def init(func):
    return func

static = classmethod
protected = init
volatile = init
final = init
private = init
constructor = init

String = "".__class__
    
        
def typed(*types):
    def dummy(func):
        return func
    return dummy
    
def dispatch_init(self,*a,**kw):
    pass

class Dummy(object):
    pass

System = Dummy()
System.out = Dummy()

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


