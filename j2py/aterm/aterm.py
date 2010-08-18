#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""Implementation of ATermDecoder

hacked from JSONDecoder code
"""
import re
from itertools import ifilter
from exceptions import ValueError

__all__ = ['ATerm','decode']

DEBUG=False

FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL

import sys

class Encodable(object):
    pass

class AString(unicode,Encodable):
    def encode(self):
        return encode_string(self)
    
class ATerm (list,Encodable):
    def __init__(self,name,params=[],annotation=None):
        self.up = None
        self.name = name
        self.extend(params)
        self.annotation=annotation
        self._update_children()

    def __str__(self): return self.encode()

    def encode(self):
        args = [encode(i) for i in self]
        if self.annotation is None:
            return u"%s(%s)" % ( self.name, u','.join(args) )
        else:
            return u"%s(%s){%s}" % (
                self.name,
                u','.join(args),
                encode(self.annotation)
            )

    def __setitem__(self,i,y):
        if y.__class__ is str:
            y = AString(y)
        elif y.__class__ is list:
            y = AList(y)
        if isinstance(y,ATerm):
            y.up = self
        list.__setitem__(self,i,y)

    def append(self,y):
        if y.__class__ is str:
            y = AString(y)
        elif y.__class__ is list:
            y = AList(y)
        if isinstance(y,ATerm):
            y.up = self
        list.append(self,y)

    def insert(self,i,y):
        if y.__class__ is str:
            y = AString(y)
        elif y.__class__ is list:
            y = AList(y)
        if isinstance(y,ATerm):
            y.up = self
        list.insert(self,i,y)

    def extend(self,l):
        for i in l:
            self.append(i)

    #TODO: write further setters ...

    def _update_children(self):
        # hm, not needed any further ... ?
        # if all setters set up ...
        return
        "sets up pointer on children to self"
        for c in self:
            if isinstance(c,(ATerm,AList)):
                c.up = self
                c._update_children()

    def __eq__(self,other):
        ##TODO: hmm, why do I have to define this function ???
        return self is other

    def walk(self):
        "returns iterator over all subnodes"
        yield self
        for c in self:
            if isinstance(c,ATerm):
                for i in c.walk():
                    yield i

    def walkback(exp):
        """
        returns iterator over all nodes before node exp


        """
        if exp.up is None:
            raise StopIteration()
        pos = exp.pos()-1
        exp = exp.up
        while pos>=0:
            yield exp[pos]
            pos -= 1
        yield exp
        for n in exp.walkback():
            yield n


    def findall(self,name):
        """
        returns all subnodes with name 'name'

        name can be a string or a list of strings
        """
        if not isinstance(name,list):
            name = [name]
        for i in self.walk():
            if isinstance(i,ATerm) and i.name in name:
                yield i

    def findfirst(self,name):
        """
        returns first subnode with name 'name'

        name can be a string or a list of strings
        """
        return self.findall(name).next()

    def __getattr__(self,name):
        if name[0:1].isupper():
            try:
                return self.findfirst(name)
            except StopIteration:
                raise RuntimeError("node named %s not found in %s" % (name,self))
        else:
            raise AttributeError


    def pos(self):
        "returns self position in parent"
        return self.up.index(self)

    def replace(self,new_node):
        "replace self with new_node on parent"
        up = self.up
        up[self.pos()] = new_node
        if isinstance(new_node,ATerm): new_node.up = up

    def parents(exp):
        "iterates over the parents of exp"
        while exp.up is not None:
            yield exp.up
            exp = exp.up

    def path(exp,join=None):
        "gives a list of parent names of node exp, concatenated by join, if given"
        res = [ p.name for p in exp.parents() ]
        res.reverse()
        if join is None:
            return res
        return join.join(res)

    def copy(self):
        "returns a new copy of self"
        return decode(self.encode())


class AList(ATerm,Encodable):
    def __init__(self):
        ATerm.__init__(self,'[]')
    def encode(self):
        return u'[%s]' % (u','.join([encode(l) for l in self]))

class ATuple(ATerm,Encodable):
    def __init__(self):
        ATerm.__init__(self,'()')
    def encode(self):
        return u'(%s)' % (u','.join([encode(l) for l in self]))

def debug(msg):
    if DEBUG:
        print "DEBUG:",msg

def linecol(doc, pos):
    lineno = doc.count('\n', 0, pos) + 1
    if lineno == 1:
        colno = pos
    else:
        colno = pos - doc.rindex('\n', 0, pos)
    return lineno, colno

def errmsg(msg, doc, pos, end=None):
    lineno, colno = linecol(doc, pos)
    if end is None:
        fmt = '%s: line %d column %d (char %d)'
        return fmt % (msg, lineno, colno, pos)
    endlineno, endcolno = linecol(doc, end)
    fmt = '%s: line %d column %d - line %d column %d (char %d - %d)'
    return fmt % (msg, lineno, colno, endlineno, endcolno, pos, end)


STRINGCHUNK = re.compile(r'(.*?)(["\\])', FLAGS)
BACKSLASH = {
    '"': u'"', '\\': u'\\', '/': u'/',
    'b': u'\b', 'f': u'\f', 'n': u'\n', 'r': u'\r', 't': u'\t',
}

DEFAULT_ENCODING = "utf-8"

def scanstring(s, end, encoding=None, strict=True, _b=BACKSLASH, _m=STRINGCHUNK.match):
    """Scan the string s for a JSON string. End is the index of the
    character in s after the quote that started the JSON string.
    Unescapes all valid JSON string escape sequences and raises ValueError
    on attempt to decode an invalid string. If strict is False then literal
    control characters are allowed in the string.

    Returns a tuple of the decoded string and the index of the character in s
    after the end quote."""
    if encoding is None:
        encoding = DEFAULT_ENCODING
    chunks = []
    _append = chunks.append
    begin = end - 1
    while 1:
        chunk = _m(s, end)
        if chunk is None:
            raise ValueError(
                errmsg("Unterminated string starting at", s, begin))
        end = chunk.end()
        content, terminator = chunk.groups()

        # Content is contains zero or more unescaped string characters
        if content:
            if not isinstance(content, unicode):
                content = unicode(content, encoding)
            _append(content)
        # Terminator is the end of string, a literal control character,
        # or a backslash denoting that an escape sequence follows
        if terminator == '"':
            break
        elif terminator != "\\":
            if strict:
                msg = "Strict Mode: Invalid control character %r at " % (terminator,)
                #msg = "Invalid control character {0!r} at".format(terminator)
                raise ValueError(errmsg(msg, s, end))
            else:
                _append(terminator)
                continue
        try:
            esc = s[end]
        except IndexError:
            raise ValueError(
                errmsg("Unterminated string starting at", s, begin))
        # If not a unicode escape sequence, must be in the lookup table
        if esc != 'u':
            try:
                char = _b[esc]
            except KeyError:
                msg = "Invalid \\escape: " + repr(esc)
                raise ValueError(errmsg(msg, s, end))
            end += 1
        else:
            # Unicode escape sequence
            esc = s[end + 1:end + 5]
            next_end = end + 5
            if len(esc) != 4:
                msg = "Invalid \\uXXXX escape"
                raise ValueError(errmsg(msg, s, end))
            uni = int(esc, 16)
            # Check for surrogate pair on UCS-4 systems
            if 0xd800 <= uni <= 0xdbff and sys.maxunicode > 65535:
                msg = "Invalid \\uXXXX\\uXXXX surrogate pair"
                if not s[end + 5:end + 7] == '\\u':
                    raise ValueError(errmsg(msg, s, end))
                esc2 = s[end + 7:end + 11]
                if len(esc2) != 4:
                    raise ValueError(errmsg(msg, s, end))
                uni2 = int(esc2, 16)
                uni = 0x10000 + (((uni - 0xd800) << 10) | (uni2 - 0xdc00))
                next_end += 6
            char = unichr(uni)
            end = next_end
        # Append the unescaped character
        _append(char)

    s = u''.join(chunks)
    return AString(s), end

match_whitespace = re.compile(r'[ \t\n\r]*', FLAGS).match
WHITESPACE = ' \t\n\r'

match_ID = re.compile(r'[A-Za-z]+[A-Za-z0-9]*', FLAGS).match

NUMBER_RE = re.compile(
    r'(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?',
    (re.VERBOSE | re.MULTILINE | re.DOTALL))
match_number = NUMBER_RE.match

ID_RE = re.compile(
    r'([A-Za-z]+[0-9_A-Za-z]*)',
    (re.VERBOSE | re.MULTILINE | re.DOTALL))

encoding = 'utf-8'
strict = True

def expect(string,idx,s):
    idx = skip_whitespace(string,idx)
    if not string[idx:idx+len(s)] == s:
        raise ValueError( errmsg("Expecting "+s, string, idx))
    else:
        return idx+len(s)

def skip_whitespace(string,idx):
    if idx<len(string) and string[idx] in WHITESPACE:
        m = match_whitespace(string,idx)
        #debug("skip whitespace %i" % (m.end()) )
        return m.end()
    return idx

def scan(string, idx):

    idx = skip_whitespace(string,idx)

    nextchar = string[idx:idx+1]

    if nextchar == None:
        return None
    if nextchar == '"':
        return scanstring(string, idx + 1, encoding, strict)
    elif nextchar == '[':
        l,idx = parse_list( string, idx + 1,']' )
        return ( l, idx )
    elif nextchar == '(':
        l,idx = parse_list( string, idx + 1,')' )
        res = ATuple()
        res.extend(l)
        return ( res , idx )

    m = match_number(string, idx)
    if m is not None:
        integer, frac, exp = m.groups()
        if frac or exp:
            res = float(integer + (frac or '') + (exp or ''))
        else:
            res = int(integer)
        return res, m.end()

    m = match_ID(string,idx)
    if m is not None:
        id_ = string[ m.start() : m.end() ]
        idx = m.end()
        if string[idx:idx+1] != '(':
            return ( ATerm(id_), m.end() )
        idx = expect(string,idx,'(')
        params,idx = parse_list(string,idx,')')
        annotation=None
        if string[idx:idx+1] == '{':
            if string[idx+1:idx+2] == '}':
               idx += 2
            else:
                annotation,idx = scan(string,idx+1)
                idx = expect(string,idx,'}')
        return ATerm(id_,params,annotation),idx

    raise ValueError( errmsg("Syntax error", string, idx))

def parse_list(string,idx,terminator):
    l = AList()
    #debug("parse list "+string[idx:idx+20])

    while True:
        idx = skip_whitespace(string,idx)
        if string[idx] == terminator:
            idx +=1
            break

        val,idx = scan(string,idx)
        #debug("append "+repr(val))
        #debug("now at "+string[idx:idx+20])
        l.append( val )
        idx = skip_whitespace(string,idx)

        nextchar = string[idx:idx+1]

        if nextchar is None:
            raise ValueError( errmsg("EOF in list, at least %s expected" % terminator, string, idx))
        if nextchar == ',':
            idx += 1
            continue
        elif nextchar == terminator:
            idx += 1
            break
        else:
            raise ValueError( errmsg("Syntax error while parsing list", string, idx))

    return l,idx


def decode(string):
    res,idx = scan(string,0)
    return res


### Encoding ###

def encode(obj):
    # this seems ugly, should everything inside a aterm be encodable ?
    if isinstance(obj,Encodable): return obj.encode()
    if isinstance(obj,int): return str(obj)
    if isinstance(obj,basestring): return encode_string(obj)

    #TODO clean this up    
    print 'missing encode for'
    print obj.__class__
    print obj
    raise RuntimeError()
    return str(obj)

ESCAPE = re.compile(r'[\x00-\x1f\\"\b\f\n\r\t]')
#ESCAPE_ASCII = re.compile(r'([\\"]|[^\ -~])')
#HAS_UTF8 = re.compile(r'[\x80-\xff]')

ESCAPE_DCT = {
    u'\\': u'\\\\',
    u'"': u'\\"',
    u'\b': u'\\b',
    u'\f': u'\\f',
    u'\n': u'\\n',
    u'\r': u'\\r',
    u'\t': u'\\t',
}

for i in range(0x20):
    #ESCAPE_DCT.setdefault(chr(i), '\\u{0:04x}'.format(i))
    ESCAPE_DCT.setdefault(chr(i), '\\u%04x' % (i,))

for i in range(128,256):
    ESCAPE_DCT.setdefault(chr(i), 'XX')

def encode_string(s):
    "Return a JSON representation of a Python string"

    def replace(match): 
        return ESCAPE_DCT[match.group(0)]
   
    if isinstance(s,str): 
        s = unicode(s,'utf8')
    elif isinstance(s,unicode):
        pass
    else:
        raise RuntimeError('bad type '+s.__class__.__name__)

    s = ESCAPE.sub(replace, s)
    return '"%s"' % s


def reverse(iterator):
    a = [i for i in iterator]
    a.reverse()
    for i in a:
        yield i

def transformation(transform):
    """
    decorator, which registers transform as a aterm transformation

    transform(ast) should either
    - do some work on ast, return ast
    - return transformation
    """

    setattr(ATerm,transform.__name__,transform)
    return transform

if __name__ == '__main__':
    import sys
<<<<<<< HEAD
    print decode ( unicode.decode(sys.stdin.read(),'utf8')).encode().encode('utf8')
=======
    print decode ( unicode.decode(sys.stdin.read(),'utf8').encode().encode('utf8')
>>>>>>> f3361c17109735dc84f1f7b46ca4f9ed77984121
    
