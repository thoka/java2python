#!/bin/bash

for src in $(find -name "*.java"); do
    echo transforming $src ...
    src=${src%.java}
    mkdir -p $(dirname $src)/out
    dst=$(dirname $src)/out/$(basename $src)
    parse-java --preserve-comments -i $src.java  > $dst.aterm
    cat $src.aterm | pp-aterm > $dst.aterm.pp
    cat $dst.aterm | ./j2py.py 2>&1 >  $dst.j2py
    cat $dst.j2py | pp-aterm >  $dst.j2py.pp
    cat $dst.j2py | ../tools/pp-java2py > $dst.py    
done
