## JavaFront/java2py

This is a hack of the JavaFront library for stratego, which
includes a pretty printer to print a python representation of a java src.

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

Next, configure it. 
On my Ubuntu system this was:

    cd java2python
    ./bootstrap
    ./configure --prefix=/usr --with-aterm=/usr --with-sdf=/usr --with-strategoxt=/usr --enable-bootstrap
    make

Test it
    tools/parse-java --preserve-comments -i contrib/python/test/bigtest.java
    tools/parse-java --preserve-comments -i contrib/python/test/bigtest.java | tools/pp-java2py
    tools/parse-java --preserve-comments -i contrib/python/test/bigtest.java | contrib/python/fixcomments.py | tools/pp-java2py

## TODO
Write and collect example java files with supposed translations.

Implement:
- java transforms to get local/static etc variables / methods right (add appropriate 'this.')




