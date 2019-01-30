# imports
import re
import unicodedata
from predicates import *


def parse_predicates(p_file):
    predicates = list()
    r_expr = re.compile('\w+')
    count = 0
    for line in p_file:
        if count == 0:
            name = re.findall(r_expr, line)[0]
            newPred = Predicate(name)
            count += 1
        elif count == 1:
            newPred.include = re.findall(r_expr, line)
            count += 1
        elif count == 2:
            newPred.exclude = re.findall(r_expr, line)
            predicates.append(newPred)
            count += 1
        else:
            count = 0

    return predicates


def lToD(i):
    return {x: i.count(x) for x in i}
