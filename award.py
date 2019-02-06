import re
from collections import Counter

class Award(object):

    def __init__(self, Predicate):
        self.name = Predicate.name
        self.relevant_tweets = list()
        self.results = {'presenters':[],
                        'nominees':[],
                        'winner':[]}
        self.include = Predicate.include
        self.exclude = Predicate.exclude
        self.stop_words = ['goldenglobes','golden','globes','','golden globes', 'tv', 'rt']

    def relevantHa(self, tweet):

        relevavantBool = True
        delimiter = ','

        for local_or_string in self.include:

            if not relevavantBool:
                break

            localBool = False
            for word in local_or_string.split(delimiter):
                if word in tweet:
                    localBool = True
                    break
            
            relevavantBool = relevavantBool and localBool

        for local_or_string in self.exclude:

            if not relevavantBool:
                break

            localBool = False
            for word in local_or_string.split(delimiter):
                if word not in tweet:
                    localBool = True
                    break
            
            relevavantBool = relevavantBool and localBool

        if relevavantBool:
            self.relevant_tweets.append(tweet)
            

    def tweetsToNouns(self, tweets):
        proper_nouns = [self.getProperNouns(tweet) for tweet in tweets]
        proper_nouns = [noun.lower() for nouns in proper_nouns for noun in nouns]
        proper_nouns = [noun for noun in proper_nouns if noun not in self.stop_words]
        return proper_nouns

    def getProperNouns(self, text):
        retList = []
        tList = text.split()
        currNoun = ''
        for word in tList:
            if word[0].isupper():
                currNoun = currNoun + ' ' + word
            elif len(currNoun) > 0:
                retList.append(currNoun.strip())
                currNoun = ''
        return retList

    def getResults(self):
        c = Counter(self.tweetsToNouns(self.relevant_tweets))
        top_five = [key for key, val in c.most_common(5)]
        self.results['nominees'] = top_five

        c = Counter(top_five)
        self.results['winner'] = c.most_common(1)[0][0]
