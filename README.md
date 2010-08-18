## java2py

Toolchain to translate java to python, using

* strategoxt / java-front to parse java
* a python aterm library and python scripts to transform java ast
* java2py, a hacked version of java-front pp-java to transform java ast to python
* a python "java" runtime, to emulate java behaviour in python

See COPYING for Copyright and License.

See http://www.strategoxt.org/Stratego/JavaFront for JavaFront

## Install on a fresh debian lenny vmware image

Use the script `install_on_debian.sh` to get everything installed and build on
a fresh debian lenny vmware image.

- get 32 bit image running from http://www.thoughtpolice.co.uk/vmware/#debian5.0

- login as root, pwd thoughtpolice

run following commands

    echo "deb http://ftp.debian.org/ testing main" >> /etc/apt/sources.list
    aptitude update
    aptitude install git-core
    git clone http://github.com/thoka/java2python.git jf2py
    cd jf2py
    bash install_on_debian_lenny.sh

at least libtool have to come from debian/testing

## Installation

Install the required dependencies

- aterm-2.5
- sdf2-bundle-2.4
- strategoxt-0.17
- java-front-0.9.1

You will find them on http://strategoxt.org/Stratego/JavaFrontRelease09

Install yaml support for python

The make files depend on bash. Check `/bin/sh --version`
if it is bash. If not, change the symlink  `/bin/sh` to point to `/bin/bash`.

Clone the git repo
    git clone git://github.com/thoka/java2python.git jf2py

Next, configure and make it.
On my Ubuntu system this was:

    cd jf2py
    ./bootstrap
    ./configure --prefix=/usr --with-aterm=/usr --with-sdf=/usr --with-strategoxt=/usr --enable-bootstrap
    make

__DO NOT__ try to install this package using `make install`

Test it
   cd j2py
   ./transform.sh
and look inside j2py/test for java files with transformation.


Play
    parse-java --preserve-comments -i j2py/test/locals1.java
    parse-java --preserve-comments -i j2py/test/locals1.java | tools/java2py
    parse-java --preserve-comments -i j2py/test/locals1.java | j2py/j2py.py | tools/java2py

    j2py/run.py j2py/test/java/out/ArithmeticDemo.py

## python AST transformations

The stratego toolchain is build out of modules, which can be chained together by piping.
As demonstrated by the third example above, python scripts can step in, to change the java AST.

## TODO / Roadmap

- make anonymous inner classes working
- convert map,list acces to python
- import neded classes in package
- create dispatchers for overwritten methods, do not use decorators as default
  (decorators are difficult to understand, debug, translate by pyjs)
- ++i etc
- add checks/translations for typecasts
- understand static imports
- do switch statement right
- java.static has to be first decorator
- add typed to interfaces
- inner assignments
- comment out @java.extends by default
- do not add self.__class__ in class_init
- do more tests for str add , seems to be broken
- remove @private, @protected
- get acces to static final attribs right: always self.attrib
- make install
- do java.typed right for VarArityParam (see LoopStyles)
- find a way to translate statements to produce no output
- implement HashMap
- file bug report for quotes not working in pp-aterm
- get empty line before @java.init

## recently done
+ boolean -> bool
+ substring -> [:]
+ lastindexof -> rfind
+ make parse-java available from python
+ comment decorations out
+ comment typed out
+ remove decorations by default
+ get docstrings in interfaces and abstract classes right

### Pitfalls

- switch statement implementation uses variable "_switch".
  nested switch statemens will use the same variable and thus will not work
- Due to a bug in stratego pp-aterm, quotes in comments are not quoted by pp-aterm.
  AST of java src, which include quotes in comments will not be understood by j2py/aterm parser.
