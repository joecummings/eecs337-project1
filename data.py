#Imports
import json
import unicodedata
import regex as re

#Helper Functions
def uniConvert(uniData):
    return unicodedata.normalize('NFKD', uniData).encode('ascii','ignore')

def mostCommon(lst):
    return max(lst,key=lst.count)

def lstToCount(src):
    return dict([ (i, src.count(i)) for i in set(src)])

def relevantData(pred,key,data):
    return [uniConvert(tweet[key]) for tweet in data if pred(tweet[key])]

def gatherTweets(pred,data):
    return relevantData(pred,'text',data)

def mostCommonString(regexPattern,tweets):
    return mostCommon([filteredString for tweet in tweets for filteredString in re.findall(regexPattern, tweet)])

def makePred(l1,l2):
    localPreds = map(lambda x: lambda y: x in y,l1) + map(lambda x: lambda y: x not in y,l2)
    return lambda x: all([f(x) for f in localPreds])
    
    

#Predicates and Lists (so they don't get out of place)
hostPred = makePred(['host'],['RT'])
hostTweets = []

tvDramaPred = makePred(['drama','win','television'],['RT'])
tvDramaTweets = []

supportingTVActorPred = makePred(['best supporting actor','win'],['RT'])
supportingTVActorTweets = []

#Body / Main
fileName = "gg2013.json"

with open(fileName) as data_file:
    rawData = json.load(data_file)

for tweetDict in rawData:
    tweet = uniConvert(tweetDict['text'])

    if hostPred(tweet):
        hostTweets.append(tweet)
    
    if tvDramaPred(tweet):
        tvDramaTweets.append(tweet)

    if supportingTVActorPred(tweet):
        supportingTVActorTweets.append(tweet)

print mostCommonString('([A-Z][\w-]*(?:\s+[A-Z][\w-]*)+)',supportingTVActorTweets)
print mostCommonString('([A-Z][\w-]*(?:\s+[A-Z][\w-]*)+)',hostTweets)
print mostCommonString('([A-Z][\w-]*(?:\s+[A-Z][\w-]*)+)',tvDramaTweets)


#Key Lessons - overlap between categories is bad - RT's kill us - this is how confident we are / have some description of our metric

#####LIST OF AWARDS######

#cecilBdeMilleAward

# bestSupportingTVActor

# bestSupportingTVActress

# bestPerformanceActorTVComedy

# bestPerormaceActressTVComedy

# performanceActorTVDrama

# performanceActressTVDrama

# perfActorLimitedSeriesTV

# perfAcressLimitedSeriesTC

# bestLimitedSeriesTV

# bestTVSeriesComedy

# bestTVdrama - included

# bestOGSongMovie

# OGScoreMovie

# movieForeignLanguage

# movieAnimated

# screenplay

# director

# perfActorSupportMovie

# perfActressSupporRoleMovie

# perfActorMovieComedy

# perfActressMovieComedy

# perfActorMovieDrama

# perfActressMovieDrama

# movieComedy

# movieDrama   #


# def makeInPred(lst):
#     return map(lambda x: lambda y: x in y,lst) 

# def makeNotInPred(lst):
#     return map(lambda x: lambda y: x not in y,lst)





