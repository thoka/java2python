class Annotation(object):

    def __init__(self,**kw):
        pass
        

def annotated(annotation):

    def helper(klass):
        return klass
        
    return helper
