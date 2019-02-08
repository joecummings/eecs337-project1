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

# def makeDressedPredicates():
#     bestInclude = ['best,great,incredible','dress,dressed,clothing']
#     bestExclude = ['RT']
#     worstInclude = ['worst,terrible,gross','dress,dressed,clothing']
#     worstExclude = ['RT'] 
#     predicates = [Predicate('Best Dressed'),Predicate('Worst Dressed')]
#     predicates[0].include = bestInclude
#     predicates[0].exclude = bestExclude
#     predicates[1].include = worstInclude
#     predicates[1].exclude = worstExclude
#     return predicates

def main():
    now = time.time()
    data_file_name = 'gg2013.json'
    categories_file_name = 'ggCategories.csv'
    awards = list()

    with open(categories_file_name, newline='\n') as f:
        predicates = [ category[0] for category in list(csv.reader(f))]

    # predicates = p_predicates('predicates.txt')
    # predicates = [] # testing line

    # award_list_predicates, len_award_list_predicates = makeAwardListPredicates()
    # predicates = predicates + award_list_predicates

    # dressed_predicates, len_dressed_predicates = makeDressedPredicates()
    # predicates = predicates + dressed_predicates

    with open(data_file_name) as data_file:
        rawData = json.load(data_file)
    
    for pred in predicates:
        # pred.makePred()
        new_award = Award(pred)

        for tweetDict in rawData:
            tweet = tweetDict['text']
            new_award.relevantHa(tweet)

        new_award.getResults()
        awards.append(new_award)
    
    print(time.time() - now)
    for a in awards:
        print(a.results['winner'], a.name) 

    for p in ['Best Dressed','Worst Dressed']:

        new_award = Award(p)
        for tweetDict in rawData:
            tweet = tweetDict['text']
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
        Image.open(paths[keywords][0]).show()
            
if __name__ == "__main__":
    main()

