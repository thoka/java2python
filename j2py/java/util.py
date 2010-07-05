class Collection(list):
    def add(self,o):
        self.append(o)
      
    def iterator(self):
        return Iterator(self)


class List(Collection):
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
            

class ArrayList(Collection):
    def __init__(self,typ):
        self._typ = typ
        
                
class Arrays(object):
    @classmethod
    def asList(self,*a):
        res = List()
        res.extend(a)
        return res
                             

