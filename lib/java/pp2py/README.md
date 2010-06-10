This is a hacked version of the stratego/java-front pp-java source files,
which produce python output.

## Installation

To get it running, you fist have to get the current svn of java-front:

    $ svn checkout https://svn.strategoxt.org/repos/StrategoXT/java-front/trunk java-front-python

Install the required build dependencies for java-front

- aterm-2.5
- sdf2-bundle-2.4
- strategoxt-0.17 


You will find them on http://strategoxt.org/Stratego/JavaFrontRelease09

The make files depend on bash. Check `/bin/sh --version`
if it is bash. If not, change the symlink  `/bin/sh` to point to `/bin/bash`.

Next, configure java-front.
On my Ubuntu system this was:

    $ cd java-front-python
    $ ./bootstrap
    $ ./configure --prefix=/usr --with-aterm=/usr --with-sdf=/usr --with-strategoxt=/usr --enable-bootstrap
    $ make

Test it
    $ tools/parse-java -i test/pp/Foo.java
    $ tools/parse-java -i test/pp/Foo.java | tools/pp-java

Now install this git over java-front-python/lib/java/pp
    $ cd lib/java
    $ mv pp pp-java
    $ git clone git@github.com:thoka/java2python.git pp-py
    $ mkdir pp
    $ cp -r pp-java/* pp
    $ cp -r pp-py/* pp
    $ cp -r pp-py/.git pp
    $ cd ../..

Make again
    $ make

Now pp-java should output python
    $ tools/parse-java -i test/pp/Foo.java | tools/pp-java

## TODO
- change it to be less hack like. At least the binary should not be named `pp-java` ( `pp-java2python` ?)

 





