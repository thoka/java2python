#!/bin/bash

cd $(dirname "$0")

for src in $(find -name "*.java"); do
    echo transforming $src ...
    src=${src%.java}
    mkdir -p $(dirname $src)/out
    dst=$(dirname $src)/out/$(basename $src)
    ../tools/parse-java --preserve-comments -i $src.java  > $dst.aterm
    _src=$(dirname $src)/out/$(basename $src)
    cat $_src.aterm | pp-aterm > $dst.aterm.pp
    cat $dst.aterm | ./j2py.py 2>&1 >  $dst.j2py
    cat $dst.j2py | pp-aterm >  $dst.j2py.pp
    cat $dst.j2py | ../tools/java2py > $dst.py    
done


