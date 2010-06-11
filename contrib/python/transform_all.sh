#!/bin/bash


for src in $(find -name "*.java"); do
    echo transforming $src ...
    parse-java --preserve-comments -i $src  > $src.aterm
    cat $src.aterm | pp-aterm > $src.aterm.pp
    cat $src.aterm | ./j2py.py 2>&1 >  $src.j2py
    cat $src.j2py | ../../tools/pp-java2py > $src.py    
done
