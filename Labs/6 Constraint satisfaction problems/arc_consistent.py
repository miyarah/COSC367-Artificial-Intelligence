# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 21:11:52 2020

@author: Amanda
"""

import itertools, copy 
from csp import *

def arc_consistent(csp):
    """Takes a CSP object and returns a new CSP object that is arc
    consistent (and also consequently domain consistent).
    
    """
    csp = copy.deepcopy(csp)
    tda = {(x, c) for c in csp.constraints for x in scope(c)}
    while tda:
        x, c = tda.pop()
        ys = list(scope(c) - {x})
        new_domain = set()
        for xval in csp.var_domains[x]:
            assignment = {x: xval}
            for yvals in itertools.product(*[csp.var_domains[y] for y in ys]):
                assignment.update({y: yval for y, yval in zip(ys, yvals)})
                if satisfies(assignment, c):
                    new_domain.add(xval)
                    break
        if csp.var_domains[x] != new_domain:
            csp.var_domains[x] = new_domain
            for cprime in set(csp.constraints) - {c}:
                if x in scope(cprime):
                   for z in scope(cprime):
                       if x != z:
                           tda.add((z, cprime))
    return csp


# # test 1
# simple_csp = CSP(
#     var_domains={x: set(range(1, 5)) for x in 'abc'},
#     constraints={
#         lambda a, b: a < b,
#         lambda b, c: b < c,
#         })

# csp = arc_consistent(simple_csp)
# for var in sorted(csp.var_domains.keys()):
#     print("{}: {}".format(var, sorted(csp.var_domains[var])))
    
    
# # test 2
# csp = CSP(var_domains={x:set(range(10)) for x in 'abc'},
#           constraints={lambda a,b,c: 2*a+b+2*c==10}) 

# csp = arc_consistent(csp)
# for var in sorted(csp.var_domains.keys()):
#     print("{}: {}".format(var, sorted(csp.var_domains[var])))