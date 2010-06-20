class Enum(object):
    @classmethod
    def __iter__(self):
        for i in self._items:
            yield i
        
class EnumItem(object):

    def __init__(self,enum_class,index,name):
        self.enum_class = enum_class
        self.index = index
        self.name = name
        self.enum_class.pos[self]=index

    def __repr__(self):
        return self.name
        
def enum(*l):
    def decorate(_class):
        _class.pos = {}
        print "decorate",l,_class
        if len(l)==1:
            names = [i.strip() for i in l[0].split(",")] 
        else:
            names = l 
        _class._items = [EnumItem(_class,i,n) for i,n in enumerate(names)]
        for i in _class._items:
            setattr(_class,i.name,i)
        return _class()
        
    return decorate

def test():

    @enum("SUNDAY,MONDAY,TUESDAY,WEDNESDAY,THURSDAY,FRIDAY,SATURDAY")    
    class Day(Enum):
        pass
            
    for i in Day:
        print i 
        
        
    
    
    
