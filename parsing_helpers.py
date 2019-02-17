# imports
import re
import unicodedata
import nltk
from imdb import IMDb
ia = IMDb()
import pickle
import string

actors = {}
with open('actors.pickle', 'rb') as handle:
    actors = pickle.load(handle)

movies = {}
with open('movies.pickle', 'rb') as handle:
    movies = pickle.load(handle)

def uniToAscii(uni_str):
  return unicodedata.normalize('NFKD', uni_str).encode('ascii','ignore')

def proper_noun_check_winner(noun_type,noun):
  if noun_type == 'art':
    #flipped
    return not noun in actors
  elif noun_type == 'person':
    return not noun in movies
  else:
    return None

def proper_noun_check_nominees(noun_type,noun):
  if noun_type == 'art':
    return noun in movies
  elif noun_type == 'person':
    return noun in actors
  else:
    return None

def trimPunc(arg_str):
  translator = str.maketrans('', '', string.punctuation)
  return arg_str.translate(translator)

def parseTweet(tweet):
    bad_characters = ['.','-','_','&','~',',', '\\','?','!',';']

    init_res = nltk.tokenize.casual.casual_tokenize(tweet)
    for i, word in enumerate(init_res):
        # init_res[i] = word.lower()
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

def pset(myset):
  if not myset: # Empty list -> empty set
    return [set()]

  r = []
  for y in myset:
    sy = set((y,))
    for x in pset(myset - sy):
      if x not in r:
        r.extend([x, x|sy])
  return r

def allNGrams(lst):
  return [' '.join(list(x)) for x in pset(set(lst))]

# def dToSubList(d):
#     retL = []
#     for key,value in d.item():
#         local_list = [(k, v) for (k, v) in D.iteritems() if key in k]
#         local_key = max(map(len, [k for (k,v) in local_list]))
#         local_value = sum([v for (k,v) in local_list])
#         retL.extend([local_value for i in range(local_key)])
#     return retL
