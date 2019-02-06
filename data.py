# imports
import json
import re
from parsing_helpers import *
from award import *
import time

types = ['presenters', 'nominees', 'winner']

def main():
    now = time.time()
    fileName = 'gg2013.json'
    results = {}
    awards = list()

    predicates = p_predicates('predicates.txt')

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
    
    print(results)
    return results
        
            
if __name__ == "__main__":
    main()

