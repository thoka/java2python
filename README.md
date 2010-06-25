## JavaFront/java2py

This is a hack of the JavaFront library for stratego, which
includes a pretty printer to print a python representation of a java src.

This project is in an early stage. Basic translation is working.
You can not expect to get full java2python translation.

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

Install the required build dependencies for java-front

- aterm-2.5
- sdf2-bundle-2.4
- strategoxt-0.17 

You will find them on http://strategoxt.org/Stratego/JavaFrontRelease09

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

- Write and collect example/test java files with supposed translations.
  - class initialization for all java types, see Class2.java
  
- Complete list of not working issues

### Currently broken
 
- class initializing
- interfaces
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


- do ... while
- add static attr init into class
- add __init__
- elif 
- get some Verbatim(pre,ast,post) token into pp-java2py to be able to write raw text into translation
- switch statement is working
- add some magic to call main methods, to be able to do tests by comparing output of java and translated java 
  
  
