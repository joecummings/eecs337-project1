# imports
import json
import re
from parsing_helpers import *
from award import *
import time

def main():
    now = time.time()
    fileName = 'gg2013.json'
    awards = list()

    with open('predicates.txt') as p_file:
        predicates = parse_predicates(p_file)

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
            
if __name__ == "__main__":
    main()

