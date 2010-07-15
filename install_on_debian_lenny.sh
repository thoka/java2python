#!/bin/bash

# install dependencies on debian lenny/testing, 
# then build

aptitude install git-core bzip2 autoconf libtool pkg-config make build-essential \
    python python-yaml openjdk-6-jdk

mkdir install
cd install

wget ftp://ftp.strategoxt.org/pub/stratego/StrategoXT/strategoxt-0.17/debian50i386/aterm_2.5-1_i386.deb
wget ftp://ftp.strategoxt.org/pub/stratego/StrategoXT/strategoxt-0.17/debian50i386/sdf2-bundle_2.4-1_i386.deb
wget ftp://ftp.strategoxt.org/pub/stratego/StrategoXT/strategoxt-0.17/debian50i386/strategoxt_0.17-1_i386.deb
wget ftp://ftp.strategoxt.org/pub/stratego/StrategoXT/strategoxt-0.17/debian50i386/java-front_0.9-1_i386.deb
 
dpkg -i aterm_2.5-1_i386.deb
dpkg -i sdf2-bundle_2.4-1_i386.deb
dpkg -i strategoxt_0.17-1_i386.deb
dpkg -i java-front_0.9-1_i386.deb

cd ..
bash rebuild.sh

echo "look for examples in ./j2py/test"



