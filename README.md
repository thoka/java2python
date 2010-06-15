## JavaFront/java2py

This is a hack of the JavaFront library for stratego, which
includes a pretty printer to print a python representation of a java src.

This project is in an early stage. Basic translation is working.
You can not expect to get full java2python translation.

See COPYING for Copyright and License.

See http://www.strategoxt.org/Stratego/JavaFront for JavaFront
 
## Installation

Install the required build dependencies for java-front

- aterm-2.5
- sdf2-bundle-2.4
- strategoxt-0.17 

You will find them on http://strategoxt.org/Stratego/JavaFrontRelease09

The make files depend on bash. Check `/bin/sh --version`
if it is bash. If not, change the symlink  `/bin/sh` to point to `/bin/bash`.

Clone the git repo
    git clone git@github.com:thoka/java2python.git java2python

Next, configure and make it. 
On my Ubuntu system this was:

    cd java2python
    ./bootstrap
    ./configure --prefix=/usr --with-aterm=/usr --with-sdf=/usr --with-strategoxt=/usr --enable-bootstrap
    make

__DO NOT__ try to install this package using `make install` 

Test it
   cd j2py
   ./transform_all.sh
and look inside j2py/test for java files with transformation.
   

Play
    tools/parse-java --preserve-comments -i j2py/test/locals1.java
    tools/parse-java --preserve-comments -i j2py/test/locals1.java | tools/java2py
    tools/parse-java --preserve-comments -i j2py/test/locals1.java | j2py/j2py.py | tools/java2py

    j2py/run.py j2py/test/java/out/ArithmeticDemo.py
    
## python AST transformations

The stratego toolchain is build out of modules, which can be chained together by piping.
As demonstrated by the third example above, python scripts can step in, to change the java AST.
   
## TODO / Roadmap

- add static attr init into class
- get some Verbatim(pre,ast,post) token into pp-java2py to be able to write raw text into translation
- add __init__
- Write and collect example/test java files with supposed translations.
- Complete list of not working issues

### Currently broken
 
- class initializing
- subcass parent scope access,  Test needed
- post/pre decr/incr, Test needed
- enums
- ...
- make install
 
### Pitfalls

- switch statement implementation uses variable "_switch". 
  nested switch statemens will use the same variable and thus will not work
- Due to a bug in stratego pp-aterm, quotes in comments are not quoted by pp-aterm.
  AST of java src, which include quotes in comments will not be understood by j2py/aterm parser.
  
### recently done

- switch statement is working
- add some magic to call main methods, to be able to do tests by comparing output of java and translated java 
  
  
