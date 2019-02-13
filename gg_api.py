'''Version 0.35'''
import data
import json

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama',
    'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy',
    'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

try:
    with open('results.json', 'r') as fp:
        results = json.load(fp)
except Exception:
    results = {}


def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
   
    res = results[year]
    hosts = res['hosts']
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    
    awards = []
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

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here


    import csv
    with open('givencategories.csv', 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(OFFICIAL_AWARDS_1315)
    print("Pre-ceremony processing complete.")
    
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    
    results['2013'] = data.main()
    with open('results.json', 'w') as fp:
        json.dump(results, fp)

    return

if __name__ == '__main__':
    main()
