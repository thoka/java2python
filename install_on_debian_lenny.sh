#!/bin/bash

aptitude install openssh-server sudo
aptitude install git-core bzip2 autoconf libtool pkg-config make python python-yaml

cd
mkdir install
cd install

wget ftp://ftp.strategoxt.org/pub/stratego/StrategoXT/strategoxt-0.17/debian50i386/aterm_2.5-1_i386.deb
wget ftp://ftp.strategoxt.org/pub/stratego/StrategoXT/strategoxt-0.17/debian50i386/sdf2-bundle_2.4-1_i386.deb
wget ftp://ftp.strategoxt.org/pub/stratego/StrategoXT/strategoxt-0.17/debian50i386/strategoxt_0.17-1_i386.deb

dpkg -i aterm_2.5-1_i386.deb
dpkg -i sdf2-bundle_2.4-1_i386.deb
dpkg -i strategoxt_0.17-1_i386.deb

cd
git clone http://github.com/thoka/java2python.git jf2py
cd jf2py
./rebuild.sh

