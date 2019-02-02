#Imports
import json
import unicodedata
import regex as re
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import pdb

#Constants
stop_words = ['goldenglobes','golden','globes','','golden globes']

####
def tweetsToNouns(tweets):
    proper_nouns = [getProperNouns(tweet) for tweet in tweets]
    proper_nouns = [noun.lower() for nouns in proper_nouns for noun in nouns]
    proper_nouns = [noun for noun in proper_nouns if noun not in stop_words]
    return proper_nouns

def getProperNouns(text):
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

# def getProperNouns(text):
#     chunked = ne_chunk(pos_tag(word_tokenize(text)))
#     continuous_chunk = []
#     current_chunk = []
#     for i in chunked:
#         if type(i) == Tree:
#             current_chunk.append(" ".join([token for token, pos in i.leaves()]))
#         elif current_chunk:
#             named_entity = " ".join(current_chunk)
#             if named_entity not in continuous_chunk:
#                 continuous_chunk.append(named_entity)
#                 current_chunk = []
#         else:
#             continue
#     named_entity = " ".join(current_chunk)
#     if named_entity not in continuous_chunk:
#         continuous_chunk.append(named_entity)
#         current_chunk = []
#     return continuous_chunk

print getProperNouns('Game Change wins #GoldenGlobe for best miniseries/ tv movie. #GoldenGlobes')

def lToD(i):
    return {x:i.count(x) for x in i}

def mostCommon(lst):
    return max(lst,key=lst.count)

def mostCommonString(regexPattern,tweets):
    return mostCommon([filteredString for tweet in tweets for filteredString in re.findall(regexPattern,tweet)])

def uniConvert(uniData):
    return unicodedata.normalize('NFKD', uniData).encode('ascii','ignore')

def makePred(l1,l2):
    localPreds = map(lambda x: lambda y: x in y,l1) + map(lambda x: lambda y: x not in y,l2)
    return lambda x: all([f(x) for f in localPreds]) 
####

###
hostPred = makePred(['host'],['RT'])
hostTweets = []

tvDramaPred = makePred(['drama','television'],['RT','actor','actress','actriz']) or makePred(['drama','tv'],['RT','actor','actress']) 
tvDramaTweets = []

supportingTVActorPred = makePred(['supporting', 'actor','win'],['RT','tv','television'])
supportingTVActorTweets = []

bestPicturePred = makePred(['best','picture','drama','win'],['RT'])
bestPictureTweets = []

tvLimitedPred = makePred(['mini','series','tv'],['RT','actor','actress']) or makePred(['mini','series','television'],['RT','actor','actress'])# or makePred(['picture','tv'],['RT']) or makePred(['picture','television'],['RT']) 
tvLimitedTweets = [] 
######

fileName = "gg2013.json"

with open(fileName) as data_file:
    rawData = json.load(data_file)

for tweetDict in rawData:
    tweet = uniConvert(tweetDict['text'])
    # tweet = tweet.lower()

    if tvLimitedPred(tweet):
        # print 'hi'
        tvLimitedTweets.append(tweet)

    if hostPred(tweet):
        hostTweets.append(tweet)
    
    if tvDramaPred(tweet):
        tvDramaTweets.append(tweet)

    if supportingTVActorPred(tweet):
        supportingTVActorTweets.append(tweet)

    if bestPicturePred(tweet):
        bestPictureTweets.append(tweet)

print mostCommon(tweetsToNouns(bestPictureTweets))
print mostCommon(tweetsToNouns(supportingTVActorTweets))
print mostCommon(tweetsToNouns(tvDramaTweets))
print mostCommon(tweetsToNouns(hostTweets))
print mostCommon(tweetsToNouns(tvLimitedTweets))

# print bestPictureTweets

# pdb.set_trace()

# print tvLimitedTweets
# #get list of list of strings
# relStrings = [getProperNounsDan(tweet) for tweet in tvLimitedTweets]
# print relStrings

# # flatten and lower
# relStrings = [string.lower() for strings in relStrings for string in strings]

# # filter
# stop_words = ['goldenglobes','golden','globes','','golden globes']
# relStrings = [string for string in relStrings if string not in stop_words]

# print relStrings
# print lToD(relStrings)

# print mostCommon(relStrings)

# print mostCommonString('([A-Z][\w-]*(?:\s+[A-Z][\w-]*)+)',bestPictureTweets)
# print mostCommonString('([A-Z][\w-]*(?:\s+[A-Z][\w-]*)+)',supportingTVActorTweets)
# print mostCommonString('([A-Z][\w-]*(?:\s+[A-Z][\w-]*)+)',hostTweets)
# print mostCommonString('([A-Z][\w-]*(?:\s+[A-Z][\w-]*)+)',tvDramaTweets)



# print relStrings
# print lToD(relStrings)
# print mostCommonString('([A-Z][\w-]*(?:\s+[A-Z][\w-]*)+)',bestPictureTweets)

