#Imports
import json
import unicodedata
import regex as re

#Helper Functions
def uniConvert(uniData):
    return unicodedata.normalize('NFKD', uniData).encode('ascii','ignore')

def mostOften(lst):
    return max(lst,key=lst.count)

def lstToCount(src):
    return dict([ (i, src.count(i)) for i in set(src)])

def relevantData(pred,key,data):
    return [uniConvert(tweet[key]) for tweet in data if pred(tweet[key])]

def relTweets(pred,data):
    return relevantData(pred,'text',data)

#Predicates and Lists (so they don't get out of place)

hostPred = (lambda x: 'host' in x and 'RT' not in x)
hostTweets = []

tvDramaPred = (lambda x: 'RT' not in x and 'drama' in x and 'win' in x and 'television' in x)
tvDramaTweets = []

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

namesOfHostTweets = [ re.findall('([A-Z][\w-]*(?:\s+[A-Z][\w-]*)+)', tweet) for tweet in hostTweets]
hostNames = [name for names in namesOfHostTweets for name in names]
print mostOften(hostNames)

tvDramaNames = [ re.findall('([A-Z][\w-]*(?:\s+[A-Z][\w-]*)+)', tweet) for tweet in tvDramaTweets]
tvDramaNamesFlattened = [name for names in tvDramaNames for name in names]
print mostOften(tvDramaNamesFlattened) #this will come close though!


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




