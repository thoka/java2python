#!/bin/bash

cd $(dirname "$0")
scriptpath=$PWD
logfile=$scriptpath/transform.log

transform() {
    local src=$1
    echo "- transforming $src ..."
    src=${src%.java}
    mkdir -p $(dirname $src)/out
    local dst=$(dirname $src)/out/$(basename $src)
    $scriptpath/../tools/parse-java --preserve-comments -i $src.java  > $dst.aterm
    local _src=$(dirname $src)/out/$(basename $src)
    cat $_src.aterm | pp-aterm > $dst.aterm.pp
    cat $dst.aterm | $scriptpath/j2py.py > $dst.j2py 2>&1
    cat $dst.j2py | pp-aterm >  $dst.j2py.pp
    cat $dst.j2py | $scriptpath/../tools/java2py > $dst.py    
}

compile_and_run() {
    echo "- compiling java $1 ..."
    javac $1
    local path=$(dirname $1)
    local class=$(basename ${1%.java})
    echo "- running java ... "
    pushd $path
    java $class > $class.java.run
    echo -n "- running python ... "
    local dst=out/$class.py
    $scriptpath/run.py $dst > $dst.run
    ( diff $class.java.run $dst.run && echo "OK" ) || 
      ( echo "Output differs: $1" > $logfile && echo "Error" )
    popd > /dev/null
}

for src in $(find -iname "*.java"); do
    echo "## $src ###################################"
    transform $src
    compile_and_run $src
    echo
    echo 
done


