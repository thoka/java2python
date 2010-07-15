#!/bin/bash
# rebuild everything. you have to provide a suitable configuration in ./configure ...

./bootstrap
./configure --prefix=/usr --with-aterm=/usr --with-sdf=/usr --with-strategoxt=/usr --with-java-front=/usr --enable-bootstrap 
make clean && make && j2py/transform_all.sh


