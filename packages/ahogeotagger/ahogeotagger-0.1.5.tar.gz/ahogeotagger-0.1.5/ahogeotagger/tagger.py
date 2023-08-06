from . import data
import ahocorasick
import logging
import re
from operator import itemgetter

A = ahocorasick.Automaton()

def _check_word_boundaries(string1, string2):
   if re.search(r"\b" + re.escape(string1) + r"\b", string2):
      return True
   return False

def _remove_subsets(input):
    sets = sorted(input,
                key=lambda x: len(x[0]),
                reverse=True)
    ret = []
    for s in sets:
        keep = True
        for r in ret:
            if s[0] in r[0]:
                keep = False
        if keep:
            ret.append(s)     
    return ret

def init(num_cities=5000,cities=[]):
    """
    Initializes the ahocorasick automaton for searching of cities through text. For each
    row representing a city, different variations of city, state and country 
    combinations are stored as search keys. For example, San Jose, CA should 
    match the same city as San Jose CA or San Jose California or San Jose California 
    USA
    Arguments:
        num_cities: This is the upper limit to the number of cities to search through
        The default is 5000 and the maximum limit for included cities is 15000.

    Returns:

    """
    global A
    if not cities:
        cities = data.cities
    for row in cities[:num_cities]:
        #city, state, country
        c,s,k = [r.lower() for r in row[1:4]]
        keys = [
                f'{k}',
                f'{c}, {s}, {k}',
                f'{c} {s} {k}',
                f'{c} {s}',
                f'{c}, {s}',
                f'{c} {k}',
                f'{c}, {k}',
                f'{c}'    
        ]
        if s in data.us_state_abbrev:
            a = data.us_state_abbrev[s]
            keys.extend(
                [
                 f'{c}, {a}, {k}',
                 f'{c} {a} {k}',
                 f'{c} {a}',
                 f'{c}, {a}'
                ]
            ) 
        for i,key in enumerate(keys):
            if not key in A:
                if i == 0:
                    A.add_word(k,(k,['','','',row[3],row[4],row[5],0,0,0]))
                else:           
                    A.add_word(key,(key,row))
    A.make_automaton()



def search(text):
    """
    Searches the given string for names of cities and countries in an
    efficient and case-insensitive manner. 
    Arguments:
        text: The input string for searching. It can contain location names
            in any format such as "San Francisco, CA" or "san francisco" or
            "california" or "United States".
        
    Returns:
        List of tuples containing matching locations.
        Each tuple has the format
        (start_index,end_index,city,state,country,iso2,iso3,population,lat,lng)
        where start and end_index indicate the boundaries of the match in the 
        source string
    """
    if(len(A) == 0):
        logging.warning(u"Tagger not initialized. \
            Initializing it with top 5000 cities.")
        init(num_cities=5000)

    found = []
    for end_index, (key,record) in A.iter(text.lower()):
        start_index = end_index - len(key) + 1
        match = text[start_index:end_index+1]
        if _check_word_boundaries(match,text):
            found.append((match,start_index,end_index)+tuple(record[1:]))
    supersets = sorted(_remove_subsets(found),key=itemgetter(2))
    return [t[1:] for t in supersets]


