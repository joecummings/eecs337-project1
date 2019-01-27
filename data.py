#Imports
import json
import unicodedata
import regex as re
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import pdb

#Imagine awardshow is a list of awards that is imported
def main():
    fileName = "gg2013.json"

    with open(fileName) as data_file:
        rawData = json.load(data_file)
    
    for tweetDict in rawData:
        tweet = uniConvert(tweetDict['text'])
        for award in award_shows:
            award.predicate(tweet)
    

# def get_continuous_chunks(text):
#      chunked = ne_chunk(pos_tag(word_tokenize(text)))
#      continuous_chunk = []
#      current_chunk = []
#      for i in chunked:
#         if type(i) == Tree:
#             current_chunk.append(" ".join([token for token, pos in i.leaves()]))
#         elif current_chunk:
#             named_entity = " ".join(current_chunk)
#             if named_entity not in continuous_chunk:
#                 continuous_chunk.append(named_entity)
#                 current_chunk = []
#         else:
#             continue
#      named_entity = " ".join(current_chunk)
#      if named_entity not in continuous_chunk:
#          continuous_chunk.append(named_entity)
#          current_chunk = []
#      return continuous_chunk
# s2 = 'Peter was in Nebraska and the Shift Series national conference, Compass Partners and fashion designer Kenneth Cole Banana Boat'
# print get_continuous_chunks(s2)
# pdb.set_trace()
    
#Predicates and Lists (so they don't get out of place)
hostPred = makePred(['host'],['RT'])
hostTweets = []

tvDramaPred = makePred(['drama','win','television'],['RT'])
tvDramaTweets = []

supportingTVActorPred = makePred(['best supporting actor','win'],['RT'])
supportingTVActorTweets = []

bestPictureComedyPred = makePred(['best','picture','motion','comedy'],['RT'])
bestPictureTweets = []

#Body / Main


for tweetDict in rawData:
    tweet = uniConvert(tweetDict['text'])

    if hostPred(tweet):
        hostTweets.append(tweet)
    
    if tvDramaPred(tweet):
        tvDramaTweets.append(tweet)

    if supportingTVActorPred(tweet):
        supportingTVActorTweets.append(tweet)

    if bestPictureComedyPred(tweet):
        bestPictureTweets.append(tweet)

print mostCommonString('([A-Z][\w-]*(?:\s+[A-Z][\w-]*)+)',bestPictureTweets)
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





