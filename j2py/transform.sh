#!/bin/bash

JAVAC="ecj -5" # use eclipse java compiler

cd $(dirname "$0")
scriptpath=$PWD
logfile=$scriptpath/transform.log

rm $logfile

transform() {
    local src=$1
    echo "- transforming $src ..."
    src=${src%.java}
    local adir=$(dirname $src)/aterm # dir containing all intermediate aterm output
    local adst=$adir/$(basename $src)
    mkdir -p $adir
    local dst=$(dirname $src)/$(basename $src).py # where py goes
    
    #parse
    parse-java --preserve-comments -i $src.java  > $adst.aterm
    
    #do python conversions
    cat $adst.aterm | $scriptpath/j2py.py > $adst.j2py 2>&1 #
    
    #transform ast -> python
    cat $adst.j2py | $scriptpath/../tools/java2py > $dst    

    # make nice intermediate outputs
    cat $adst.aterm | pp-aterm > $adst.aterm.pp
    cat $adst.j2py  | pp-aterm > $adst.j2py.pp

}


compile_and_run() {

    #compile java

    local path=$(dirname $1)
    local class=$(basename ${1%.java})
    pushd $path > /dev/null

    if [[ "$class.java" -nt "$class.class" ]] 
    then
        echo "- compiling java $1 ..."
        $JAVAC "$class.java"
    fi
   
    #run and compare output
    if grep -q "main(\s*String" "$class.java" 
    then
    
        #run java
        echo "- running java ... "
        #grep "public static void main" $class.java && \
        
        if [[ "$class.class" -nt "$class.java.run" ]]
        then
            java -ea $class > $class.java.run
        fi
        
        #run python
        echo -n "- running python ... "
        local dst=$class.py
        $scriptpath/run.py $dst  > $dst.run 2> $logfile.tmp
        cat $logfile.tmp
        cat $logfile.tmp >> $dst.run
        #cat $logfile.tmp >> $logfile
        rm $logfile.tmp
        
        #compare output
        ( diff $class.java.run $dst.run && echo "OK" ) || 
          ( (echo "Output differs: $1" >> $logfile) && ( echo "Error") \
            && (diff $class.java.run $dst.run >> $logfile))
    fi    
   
    popd > /dev/null
}


for src in $(find test -iname "$1*.java" | sort ); do
    echo "## $src ###################################"
    echo "## $src ###################################" >> $logfile

    transform $src
    compile_and_run $src
    echo
    echo 
done


