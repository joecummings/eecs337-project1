# imports
import re
import unicodedata
from predicates import *



def p_predicates(p_file):

    with open(p_file) as content_file:
        predicates_content = content_file.read()
    preds_by_line = [pred.split('\n') for pred in predicates_content.split('\n\n') ]
    
    predicates = []
    for pred_by_line in preds_by_line:
        local_pred = Predicate(pred_by_line.pop(0))
        local_pred.include = pred_by_line[:pred_by_line.index('-')]
        local_pred.exclude = pred_by_line[pred_by_line.index('-')+1:]
        predicates.append(local_pred)
    return predicates

def lToD(i):
    return {x: i.count(x) for x in i}
