'''Version 0.35'''
import data
import json
import unicodedata
import time
import requests
import pickle

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama',
    'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy',
    'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

try:
    with open('results.json', 'r') as fp:
        results = json.load(fp)
except Exception:
    results = {}

awards = {}


def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
   
    res = results[year]
    hosts = res['hosts']
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    with open('bl' + year + '.pickle', 'rb') as handle:
        awards = pickle.load(handle)

    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    
    if year == '2013' or year == '2015':
        offish_awards = OFFICIAL_AWARDS_1315
    else:
        offish_awards = OFFICIAL_AWARDS_1819
    
    res = results[year]

    nominees = {award: res['award_data'][award]['nominees'] for award in offish_awards}
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    
    if year == '2013' or year == '2015':
        offish_awards = OFFICIAL_AWARDS_1315
    else:
        offish_awards = OFFICIAL_AWARDS_1819
    
    res = results[year]

    winners = {award: res['award_data'][award]['winner'] for award in offish_awards}
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''

    if year == '2013' or year == '2015':
        offish_awards = OFFICIAL_AWARDS_1315
    else:
        offish_awards = OFFICIAL_AWARDS_1819
    
    res = results[year]
    presenters = {award: res['award_data'][award]['presenters'] for award in offish_awards}
    return presenters

#helper for pre ceremony
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    only_ascii = only_ascii.decode('ASCII')
    return only_ascii

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    
    #Part 1

    #GRABS EVERY ACTOR/ACTRESS/DIRECTOR IN EVERY MOVIE SINCE 2012
    #print('SET YEAR IN PRE_CEREMONY') #this can edit the query! with year.... very nice :)

    query = '''PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT DISTINCT ?filmLabel ?directorLabel ?actorLabel  WHERE {
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
        ?film wdt:P31 wd:Q11424.
        ?film wdt:P161 ?cast.
        ?cast wdt:P373 ?actor.
        ?film wdt:P577 ?date.
        ?film wdt:P57 ?director
        FILTER("2012-01-01"^^xsd:dateTime <= ?date && ?date < "2019-01-01"^^xsd:dateTime).
    }
    LIMIT 100000
    '''
    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
    data = requests.get(url, params={'query': query, 'format': 'json'}).json()


    movies = {}
    actors = {}
    for record in data['results']['bindings']:
        movies[remove_accents(record['filmLabel']['value'].lower())] = True
        actors[remove_accents(record['actorLabel']['value'].lower())] = True

    with open('movies.pickle', 'wb') as handle:
        pickle.dump(movies, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('actors.pickle', 'wb') as handle:
        pickle.dump(actors, handle, protocol=pickle.HIGHEST_PROTOCOL)

    import csv
    with open('givencategories.csv', 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(OFFICIAL_AWARDS_1315)
    print("Pre-ceremony processing complete.")

    #Garbage return
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    now = time.time()

    for year in ['2013','2015', '2018', '2019']:
    # print('CHANGE GG_API.PY YEAR BACK')
    # for year in ['2013']:
        results[year] = data.main(year)
    
    with open('results.json', 'w') as fp:
        json.dump(results, fp)

    
    print(time.time() - now)
    print("------------------------------")

    return

if __name__ == '__main__':
    main()
