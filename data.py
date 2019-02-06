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

types = ['presenters', 'nominees', 'winner']

def main():
    now = time.time()
    fileName = 'gg2013.json'
    results = {}
    awards = list()

    predicates = p_predicates('predicates.txt')
    extra_predicates, len_extra_predicates = makeExtraPredicates()
    predicates = predicates + extra_predicates

    with open(fileName) as data_file:
        rawData = json.load(data_file)
    
    for pred in predicates:
        # pred.makePred()
        new_award = Award(pred)

        for tweetDict in rawData:
            tweet = tweetDict['text']
            new_award.relevantHa(tweet)

        new_award.getResults()
        if new_award.name == 'hosts':
            results['hosts'] = new_award.results['winner']
        else:
            awards.append(new_award)
    
    results['award_data'] = {}
    for award in awards:
        results['award_data'][award.name] = {}
        for t in types:
            results['award_data'][award.name][t] = award.results[t]
    
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
    
    print(time.time() - now)
    print(results)
    return results
            
if __name__ == "__main__":
    main()

