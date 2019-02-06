# imports
import re
import unicodedata
from predicates import *
import nltk

def parseTweet(tweet):
    bad_characters = ['.','-','_','&','~',',', '\\','?','!',';']

    init_res = nltk.tokenize.casual.casual_tokenize(tweet)
    for i, word in enumerate(init_res):
        init_res[i] = word.lower()
        if word in bad_characters:
            init_res[i] = ""
    
    return ' '.join([x for x in init_res if x != ""])



def p_predicates(p_file):

    with open(p_file, 'r') as content_file:
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
