import re
from parsing_helpers import lToD
class Award(object):

    def __init__(self, name):
        self.name = name
        self.include, self.exclude = self.generateIncludeExclude()
        self.relevant_tweets = list()
        # self.include = Predicate.include
        # self.exclude = Predicate.exclude
        self.nominees = list()
        self.stop_words = ['need','very','by','a','an','in','best','golden','globe','goldenglobe','golden globe','golden globes','', 'tv', 'rt','i','the']
        self.winner = ''
        self.nominees = []

    def generateIncludeExclude(self):
        include_list = []
        exclude_list = ['RT']

        include_dict = {
            'drama':'drama',
            'host':'host',
            'comedy': 'comedy,musical',
            'musical': 'comedy,musical',
            'actor':'actor',
            'actress':'actress,actriz',
            'best':'best',
            'director':'director',
            'motion':'motion,picture',
            'picture':'motion,picture',
            'supporting':'supporting,extra'
        }
        exclude_dict = {
            'actor':'actress,actriz',
            'actress':'actor'
        }

        for word in self.name.split(' '):
            word = word.lower()
            try:
                include_list.append(include_dict[word])
                exclude_list.append(exclude_dict[word])
            except:
                pass

        return include_list, exclude_list

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
        #list of list t0 list
        proper_nouns = [self.getProperNouns(tweet) for tweet in tweets]
        #flatten and lower
        proper_nouns = [noun.lower() for nouns in proper_nouns for noun in nouns]
        #filter for special case - might add some complexity but oh well
        if self.name == 'Award Show':
            proper_nouns = [noun for noun in proper_nouns if noun in self.include[0].split(',')]
        else:
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

        d = lToD(self.tweetsToNouns(self.relevant_tweets))
        for key,value in d.items():
            for key2,value2 in d.items():
                if key2 in key:
                    d[key] += d[key2]

        top_five = []
        v=list(d.values())
        k=list(d.keys())
        for i in range(5):
            index = v.index(max(v))
            top_five = k[index]
            v.pop(index)
        self.winner = top_five[0]
        self.nominees = top_five

    def mostCommon(self, lst):
        try:
            return max(lst, key=lst.count)
        except:
            return ''
