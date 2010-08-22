#!/usr/bin/env python
#-*- coding:utf-8 -*-

try:
    import syck as yaml
except:
    import yaml 
        
import os.path, logging, sys

config_data = os.path.join(os.path.dirname(__file__), "java2py.yaml")
config = yaml.load(open(config_data))

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
