#-*- coding:utf-8 -*-

import config
import aterm
import logging

logger = logging.getLogger("j2py.fix_expressions")

assign_expressions = config.config["assign-expressions"]

@aterm.transformation
def fix_assigns(ast):
    for a in ast.findall(assign_expressions):
        parents = [ p for p in a.parents() ]
        if parents[0].name != 'ExprStm':
            logging.warning("inner assign %s %s",a, [p.name for p in parents])

run = fix_assigns
