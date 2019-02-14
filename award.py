import re
from collections import Counter
from parsing_helpers import lToD, proper_noun_check

class Award(object):

    def __init__(self, name):
        self.name = name
        self.include, self.exclude = self.generateIncludeExclude()
        self.relevant_tweets = list()
        self.results = {'presenters':[],
                        'nominees':[],
                        'winner':[]}
        self.nominees = list()
        self.stop_words = ['tv','tvs','congratulations','need','very','by','a','an','in','best','golden','globe','goldenglobe','golden globe','golden globes','', 'tv', 'rt','i','the']
        self.winner = ''
        self.nominees = []
        if 'actor' in name or 'actress' in name or 'director' in name or 'score' in name:
            self.noun_type = 'person'
        else:
            self.noun_type = 'art'

    def generateIncludeExclude(self):
        include_list = []
        exclude_list = ['rt']

        include_dict = {
            'host': 'host',
            'cecil b. demille award': 'cecil',
            'generate categories': 'best motion picture',
            ##
            'presen':'jessica chastain',
            'present': 'present,presenter,presents',
            'host': 'host,hosts',
            'best dresse' : 'best,great,incredible',
            'best dressed':'dress,dressed,clothing',
            'worst dresse' : 'worst,terrible,gross',
            'worst dressed': 'dress,dressed,clothing',
            #Most controversial runner-up (cally version)
            'controversial runner-up' : 'robbed, stole, cheated, unfair, shocker',
            # funniest acceptance speech this could very well just return the best presentation speech if there is a blowout like ferrell's
            #'funniest acceptance speech' : 'funny, lol, best, speech, accepting' ,
            #crowd's favoritie presentation speech
            'crowd favorite presentation' : 'presented, speech, presenting, amazing',
            'best after party' : 'afterparty, party',
            ##Hacky
            'limited series': 'mini-series for,mini series for,miniseries for,limited series for,for television, for tv,for t.v.',
            'for television': 'mini-series for,mini series for,miniseries for,limited series for,for television, for tv,for t.v.',
            'television':'tv,television,tele,t.v.',
            'song': 'song',
            'score': 'score,composer', #do not fucking say music
            'language':'foreign,language',
            'foreign':'foreign,language',
            'animated': 'anime,animated,animate,cartoon',
            'screenplay':'screenplay',
            'drama':'drama',
            'host':'host',
            'comedy': 'comedy,musical',
            'musical': 'comedy,musical',
            'actor':'actor,performance',
            'actress':'actress,actriz,performance',
            'director':'director',
            'motion':'motion,picture',
            'picture':'motion,picture',
            'supporting':'supporting,extra'
        }
        exclude_dict = {
            'series': 'movie,motion,picture',
            'foreign': 'press',
            'actor':'actress,actriz',
            'actress':'actor'
        #for Ryan's extras
        #controversial runner up
        #funniest acceptance speech
        #crowd favorite presentation speech
        }

        for key,value in include_dict.items():
            if key in self.name.lower():
                include_list.append(value)

        for key,value in exclude_dict.items():
            if key in self.name.lower():
                exclude_list.append(value)

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

    # def mostCommon(self,lst):
    #     return max(set(lst), key=lst.count)

    def getResults(self):

        c = Counter(self.tweetsToNouns(self.relevant_tweets))
        nounsAndCounts = [(key,pair) for key,pair in c.items()]
        nounsAndCounts.sort(key=lambda x: -x[1])
        five_most_common = []

        i = 0 
        while len(five_most_common) < 5:
            try:
                name = nounsAndCounts[i][0]
                if proper_noun_check(self.noun_type,name):
                    five_most_common.append(name)
                i += 1
            except:
                break

        try:
            self.results['nominees'] = five_most_common
        except:
            self.results['nominees'] = []

        try:
            self.results['winner'] = five_most_common[0]
        except:
            self.results['winner'] = 'Larry Birmbaum'
