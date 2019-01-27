import re


class Award(object):

    def __init__(self, Predicate):
        self.name = Predicate.name
        self.relevant_tweets = list()
        self.predicate = Predicate.pred
        self.nominees = list()
        self.stop_words = ['goldenglobes','golden','globes','','golden globes', 'tv']
        self.winner = ''

    def relevantHa(self, tweet):
        if self.predicate(tweet):
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
        return max(lst, key=lst.count)
