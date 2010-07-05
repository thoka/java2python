from helpers import str
import sys

class Array(list):
    def __getattr__(self,key):
        if key == 'length':
            return len(self)
        raise Exception('key not found') #TODO raise right exception, read docs ...
               

class Class(object):
    def __init__(self,typ):
        self.typ = typ

    def getName(self):
        return self.typ.__name__

    def getInterfaces(self):
        try:
            return self.typ._interfaces
        except:
            return []
                                                                                  
class Object(object):
    
    __interfaces = []
    
    def getClass(self):
        return Class(self.__class__)


String = "".__class__

System = Object()
System.out = Object()

def println(*args):
    print "".join([ str(i) for i in args])
    
def print_(o):
    sys.stdout.write(str(o))
    sys.stdout.flush()

System.out.println = println
System.out.print_ = print_


class Interface(object):
    @classmethod    
    def getName(self):
        return self.__name__
        
class Number(object):
    pass
    
class Integer(int,Number):
    pass
    
        
class Iterator(object):

    def __init__(self,collection):
        self.pos = 0
        self.collection = collection

    def hasNext(self):
        return self.pos < len(self.collection)

    def next(self):
        self.pos += 1
        return self.collection[self.pos-1]

    def remove(self):
        self.collection.pop(self.pos-1)
        self.pos -= 1
                    

