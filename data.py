# imports
import json
import re
from parsing_helpers import *
from award import *
import time
from PIL import Image
from google_images_download import google_images_download 

#might want to include host in here?
def makeExtraPredicates():
    bestInclude = ['best,great,incredible','dress,dressed,clothing']
    bestExclude = ['RT']
    worstInclude = ['worst,terrible,gross','dress,dressed,clothing']
    worstExclude = ['RT'] 
    predicates = [Predicate('Best Dressed'),Predicate('Worst Dressed')]
    predicates[0].include = bestInclude
    predicates[0].exclude = bestExclude
    predicates[1].include = worstInclude
    predicates[1].exclude = worstExclude
    return predicates, len(predicates)

def main():
    now = time.time()
    fileName = 'gg2013.json'
    awards = list()

    predicates = p_predicates('predicates.txt')
    extra_predicates, len_extra_predicates = makeExtraPredicates()
    predicates = predicates + extra_predicates

    with open(fileName) as data_file:
        rawData = json.load(data_file)
    
    for pred in predicates:
        pred.makePred()
        new_award = Award(pred)

        for tweetDict in rawData:
            tweet = tweetDict['text']
            new_award.relevantHa(tweet)

        new_award.getWinner()
        awards.append(new_award)
    
    print(time.time() - now)
    print([(a.winner, a.name) for a in awards])

    for a in awards[:len_extra_predicates:-1]:
        awardCeremonyYear = '2013'
        keywords = a.winner + ' ' + a.name + ' '+ awardCeremonyYear
        response = google_images_download.googleimagesdownload()
        arguments = {
			"keywords": keywords,
			"limit": 1
		}
        paths = response.download(arguments) 
        Image.open(paths[keywords][0]).show()
            
if __name__ == "__main__":
    main()

