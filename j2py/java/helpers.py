# ... simulate java like output in str()
_str = str
def str(o):
    if o is None:
        return ""
    elif o is True:
        return "true"
    elif o is False:
        return "false"
    elif isinstance(o,unicode):
        return o.encode('utf8')
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
        
class synchronize(object):
    def __init__(self,lock):
        pass
    
    def __enter__(self,*a):
        #print "__enter__",a
        pass
        
    def __exit__(self,*a):
        #print "__exit__",a
        pass

