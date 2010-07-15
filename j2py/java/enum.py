class Enum(object):  
    @classmethod
    def __iter__(self):
        for i in self._items:
            yield i
        
class EnumItem(object):
    def __repr__(self):
        return self.name
        
def enum(klass):
    """
    decorator to initialise enums
    
    reads klass.init and creates 
      EnumItems for init == [string]
      klass.EnumItems(*args) for init == [(string,(args))]
    """
      
    klass.pos = {}
    klass.items = []
    
    for index,init in enumerate(klass.init):
        if isinstance(init,tuple):
            name,args = init
            item = klass.EnumItem(*args)
        else:
            name = init
            item = EnumItem()
        item.enum_class = klass
        item.index = index
        item.name = name
        klass.pos[item]=index
        setattr(klass,name,item)
        klass.items.append(item)
        
    return klass

