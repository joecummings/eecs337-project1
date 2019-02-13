# imports
import json
import re
from parsing_helpers import *
from award import *
import time
from PIL import Image
from google_images_download import google_images_download 
import csv

#might want to include host in here?
def makeAwardListPredicates():
    award_include = ['golden globes,critics choice,screen actors,academy awards,emmy,producers guild,directors guild,writers guild']
    award_exclude = ['RT']
    #Name is important
    predicates = [Predicate('Award Show')]
    predicates[0].include = award_include
    predicates[0].exclude = award_exclude
    return predicates, len(predicates)

types = ['presenters', 'nominees', 'winner']

def main():
    now = time.time()
    data_file_name = 'gg2013.json'
    categories_file_name = 'ggCategories.csv'
    awards = list()
    results = {}

    with open(categories_file_name, newline='\n') as f:
        predicates = [ category[0] for category in list(csv.reader(f))]

    with open(data_file_name) as data_file:
        rawData = json.load(data_file)
    
    for pred in predicates:
        new_award = Award(pred)

        for tweetDict in rawData:
            tweet = parseTweet(tweetDict['text'])
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
    
    print(time.time() - now)
    print(results)

    for p in ['Best Dressed','Worst Dressed']:

        new_award = Award(p)
        for tweetDict in rawData:
            tweet = parseTweet(tweetDict['text'])
            new_award.relevantHa(tweet)
        new_award.getResults()

        awardCeremonyYear = '2013'
        keywords = new_award.results['winner'] + ' ' + new_award.name + ' '+ awardCeremonyYear
        response = google_images_download.googleimagesdownload()
        arguments = {
			"keywords": keywords,
			"limit": 1
		}
        paths = response.download(arguments) 
        #Image.open(paths[keywords][0]).show()

    return results

if __name__ == "__main__":
    main()

