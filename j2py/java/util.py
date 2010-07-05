from objects import Iterator, Object
from helpers import str


class Collection(list):
    def add(self,o):
        self.append(o)
      
    def iterator(self):
        return Iterator(self)

    def __str__(self):
        return "[%s]" % (', '.join([str(i) for i in self]))
        

class List(Collection):
    pass
    
            
class ArrayList(Collection):
    def __init__(self,typ = (Object,)):
        self._typ = typ
        
                
class Arrays(object):
    @classmethod
    def asList(self,*a):
        res = List()
        res.extend(a)
        return res
                             

