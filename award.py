import re


class Award(object):

    def __init__(self, Predicate):
        self.name = Predicate.name
        self.relevant_tweets = list()
        self.include = Predicate.include
        self.exclude = Predicate.exclude
        self.nominees = list()
        self.stop_words = ['goldenglobes','golden','globes','','golden globes', 'tv', 'rt','i','the']
        self.winner = ''

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

    def getWinner(self):
        self.winner = self.mostCommon(self.tweetsToNouns(self.relevant_tweets))

    def mostCommon(self, lst):
        try:
            return max(lst, key=lst.count)
        except:
            return ''
