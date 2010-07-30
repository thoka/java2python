#!/usr/bin/env python
#-*- coding:utf-8 -*-

import syck
import os.path

config_data = os.path.join(os.path.dirname(__file__), "java2py.yaml")
config = syck.load(open(config_data))
