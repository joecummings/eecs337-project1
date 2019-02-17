# imports
import json
import re
from parsing_helpers import *
from award import *
import time
from PIL import Image
from google_images_download import google_images_download 
import csv
import pprint
import pickle


#might want to include host in here?
def makeAwardListPredicates():
    award_include = ['golden globes,critics choice,screen actors,academy awards,emmy,producers guild,directors guild,writers guild']
    award_exclude = ['RT']
    #Name is important
    predicates = [Predicate('Award Show')]
    predicates[0].include = award_include
    predicates[0].exclude = award_exclude
    return predicates, len(predicates)


def buildAwards(categories,rawData):
    awards = []
    for category in categories:
        new_award = Award(category)
        for tweetDict in rawData:
            tweet = tweetDict['text']
            # tweet = parseTweet(tweetDict['text'])
            new_award.relevantHa(tweet)
        new_award.getResults()
        awards.append(new_award)
    return awards

def main(year):

    #Parameters
    categories_file_name = 'givencategories.csv'
    data_file_name = 'gg'+year+'.json'

    #Variables
    awards = list()
    results = {}
    results['award_data'] = {}
    types = ['presenters', 'nominees', 'winner']

    #Part 0 - Gather Data
    with open(data_file_name) as data_file:
        rawData = json.load(data_file)

    #Part 1 - Host of Ceremony
    awards = buildAwards(['host'],rawData)
    results['hosts'] = list()
    results['hosts'].append(awards[0].results['nominees'][0])
    results['hosts'].append(awards[0].results['nominees'][1])
    awards = []

    
    #Parts 3-5 -  Built in Categories
    with open(categories_file_name, newline='\n') as f:
        categories = list(csv.reader(f))[0]
    awards = buildAwards(categories,rawData)
    for award in awards:
        results['award_data'][award.name] = {}
        for t in types:
            results['award_data'][award.name][t] = award.results[t]

    #Part 2 - Awards / Categories
    c = Counter(best_list)
    bl = c.most_common(min(30,len(best_list)))
    bl = [ noun for noun,count in bl]
    with open('bl' +year+ '.pickle', 'wb') as handle:
        pickle.dump(bl, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # nouns_and_counts = [(key,value) for key,value in c]
    # nouns_and_counts.sort(lambda x: -x[1])
    
    
    pprint.pprint(results,depth=3)
	
    #Part 6 Extra Awards  
    extras = ['best dressed','worst dressed','controversial','funniest'] #,'controversial runner-up', 'crowd favorite presentation', 'best after party']
    awards = buildAwards(extras,rawData)
    for new_award in awards:
        keywords = new_award.results['winner'] + ' ' + new_award.name + ' '+ year
        response = google_images_download.googleimagesdownload()
        arguments = {
	 		"keywords": keywords,
	 		"limit": 1
	 	}
        paths = response.download(arguments) 
    awards = []

    return results

if __name__ == "__main__":
    main()

