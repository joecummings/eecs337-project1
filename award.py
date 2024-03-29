import re
from collections import Counter
from parsing_helpers import lToD, proper_noun_check_winner,proper_noun_check_nominees, trimPunc

best_list = []

exclude_dict = {
    'supporting': [],
    'picture -': ['mini-series','mini series','miniseries','limited series'],
    'series': ['movie,motion,picture'],
    'foreign': ['press'],
    'actor':['actress,actriz'],
    'actress':['actor'],
    'host':['rt']
}
include_dict = {
    'funniest': ['funniest,funny,hilarious'],
    'controversial': ['controversial'],
    'cecil b. demille award': ['cecil','b','demille'],
    'present': ['present,presenter,presents'],
    'host': ['host,hosts'],
    'best dressed':['best dressed'],
    'worst dressed': ['dress,dressed,clothing','worst,terrible,gross'],
    'controversial runner-up' : ['robbed,stole,cheated,unfair,shocker'],
    'crowd favorite presentation' : ['presented,speech,presenting,amazing'],
    'best after party' : ['afterparty,party'],
    'limited series': ['mini-series,mini series for,miniseries,limited series'],
    'for television': ['mini-series,mini series for,miniseries,limited series'],
    'television': ['tv,television,tele,t.v.'],
    'song': ['song'],
    'score': ['score,composer'],
    'language': ['foreign,language'],
    'foreign': ['foreign,language'],
    'animated': ['anime,animated,animate,cartoon'],
    'screenplay': ['screenplay'],
    'drama': ['drama'],
    'comedy': ['comedy,musical'],
    'musical': ['comedy,musical'],
    'actor': ['actor,performance'],
    'actress': ['actress,actriz,performance'],
    'director': ['director'],
    'motion': ['motion,picture'],
    'picture': ['motion,picture']  
}

class Award(object):

    def __init__(self, name, year):
        self.name = name
        self.year = year
        self.include, self.exclude = self.generateIncludeExclude()
        self.relevant_tweets = list()
        self.results = {'presenters':[],
                        'nominees':[],
                        'winner':[]}
        self.nominees = list()
        self.stop_words = ['tv','tvs','congratulations','need','very','by','a','an','in','best','golden','globe','goldenglobe','golden globe','golden globes','', 'tv', 'rt','i','the']
        self.winner = ''
        self.nominees = []
        if 'score' in name:
            self.noun_type = 'music'
        elif 'cecil' in name or 'funniest' in name or 'controversial' in name or 'dressed' in name or 'host' in name or 'actor' in name or 'actress' in name or 'director' in name or 'score' in name:
            self.noun_type = 'person'
        else:
            self.noun_type = 'art'

    def generateIncludeExclude(self):
        include_list = []
        exclude_list = []

        for key,value in include_dict.items():
            if key in self.name.lower():
                for include_or in value:
                    include_list.append(include_or)

        for key,value in exclude_dict.items():
            if key in self.name.lower():
                for exclude_or in value:
                    exclude_list.append(exclude_or)

        return include_list, exclude_list

    def relevantHa(self, tweet):

        originalTweet = tweet
        tweet = tweet.lower()

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
            self.relevant_tweets.append(originalTweet)
            

    def tweetsToNouns(self, tweets):
        #list of list t0 list
        proper_nouns = [self.getProperNouns(tweet) for tweet in tweets]
        #flatten and lower
        proper_nouns = [noun.lower() for nouns in proper_nouns for noun in nouns]

        #this is fun ....
        [best_list.append(noun) for noun in proper_nouns if 'best' in noun]

        #filter for special case - might add some complexity but oh well
        if self.name == 'Award Show':
            proper_nouns = [noun for noun in proper_nouns if noun in self.include[0].split(',')]
        else:
            #experiment - making sure we can't get junk from our name
            proper_nouns = [noun for noun in proper_nouns if noun not in self.stop_words and not(bool(set(noun.split(' ')) & set(self.name.lower().split(' '))))]
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

    def mostCommon(self,lst):
        return max(set(lst), key=lst.count)


    def getResults(self):

        c = Counter(self.tweetsToNouns(self.relevant_tweets))
        nounsAndCounts = [(key,pair) for key,pair in c.items()]
        nounsAndCounts.sort(key=lambda x: -x[1])

        five_most_common = []
        i = 0 
        #Winner
        while len(five_most_common) < 1:
            try:
                name = nounsAndCounts[i][0]
                if proper_noun_check_winner(self.noun_type,name, self.year):
                    five_most_common.append(name)
                i += 1
            except:
                break
        #Nominees
        while len(five_most_common) < 5:
            try:
                name = nounsAndCounts[i][0]
                if proper_noun_check_nominees(self.noun_type,name, self.year):
                    five_most_common.append(name)
                i += 1
            except:
                break

        try:
            self.results['nominees'] = five_most_common
            if 'cecil' in self.name:
                self.results['nominees'] = []
        except:
            self.results['nominees'] = []

        try:
            winner = five_most_common[0]
            self.results['winner'] = winner

            if self.noun_type == 'person':
                exclude_dict['supporting'].append(winner)
        except:
            self.results['winner'] = 'Larry Birmbaum'

        #Presenters Code
        self.include = ['present,presents,presenting']
        self.exclude = []
        old_relevant_tweets = self.relevant_tweets
        self.relevant_tweets = []
        for tweet in old_relevant_tweets:
            self.relevantHa(tweet)

        c = Counter(self.tweetsToNouns(self.relevant_tweets))
        nounsAndCounts = [(key,pair) for key,pair in c.items()]
        nounsAndCounts.sort(key=lambda x: -x[1])

        five_most_common = []
        i = 0 
        #Presenter
        while len(five_most_common) < 1:
            try:
                name = nounsAndCounts[i][0]
                if proper_noun_check_winner(self.noun_type,name, self.year):
                    five_most_common.append(name)
                i += 1
            except:
                break

        try:
            winner = five_most_common[0]
            self.results['presenters'] = five_most_common[0]

        except:
            self.results['presenters'] = 'Jason Cohn'





        
