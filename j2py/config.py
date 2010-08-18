#!/usr/bin/env python
#-*- coding:utf-8 -*-

import syck
import os.path
import logging
import sys


config_data = os.path.join(os.path.dirname(__file__), "java2py.yaml")
config = syck.load(open(config_data))

# create logger
logger = logging.getLogger("j2py")
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler(sys.stderr)
ch.setLevel(logging.DEBUG)

# create formatter
#formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to ch
#ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
