#!/bin/bash

./bootstrap
./configure --prefix=/usr --with-aterm=/usr --with-sdf=/usr --with-strategoxt=/usr --enable-bootstrap
make clean
make

