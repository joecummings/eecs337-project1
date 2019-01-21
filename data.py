import json
import unicodedata
import regex as re

fileName = "gg2013.json"

with open(fileName) as data_file:
    rawData = json.load(data_file)


def uniConvert(uniData):
    return unicodedata.normalize('NFKD', uniData).encode('ascii', 'ignore')


def mostOften(lst):
    return max(lst, key=lst.count)

hostTweets = [uniConvert(tweet['text']) for tweet in rawData if 'host' in tweet['text']]
capitalWordsHostTweets = [re.findall('([A-Z][a-z]+)', tweet) for tweet in hostTweets]
hostCapitalWords = [word for words in capitalWordsHostTweets for word in words]
print mostOften(hostCapitalWords)


# namesOfHostTweets = [ re.findall('([A-Z][\w-]*(?:\s+[A-Z][\w-]*)+)', tweet) for tweet in hostTweets]
# hostNames = [name for names in namesOfHostTweets for name in names]
# src = hostNames
# result_dict = dict( [ (i, src.count(i)) for i in set(src) ] )
# print result_dict
# print mostOften(hostNames)
