#!/usr/bin/env python
from difflib import SequenceMatcher

similar = lambda a, b, r=0.95: SequenceMatcher(None, a.lower(), b.lower()).ratio() >= r if r is not None else SequenceMatcher(None, a.lower(), b.lower()).ratio()
find_similar_to_a_in_dict_b = lambda a, b, r=0.95: [b_key for b_key in b if similar(a, b_key, r)]
a_is_not_in_dict_b = lambda a, b, r=0.95: not find_similar_to_a_in_dict_b(a, b, r)
compare_linkers_parsed_docs = lambda a, b, n, r=0.95: [(i, a_entity) for (i, (a_doc, b_doc)) in enumerate(zip(a[0:n], b[0:n])) for a_entity in a_doc['entities'] if a_is_not_in_dict_b(a_entity, b_doc, r)]

# Below are a set of functions to map a list a to a list b 
def inverse_scoring(a_i, b_i):
    score = 1.0 / (float(abs(a_i - b_i) + 0.1 ))
    return score

# change a_index for a relative position in its list
def elements_similarity(a_i, a, a_len, b_i, b, b_len):
    return (
        inverse_scoring(float(a_i)/float(a_len),
                        float(b_i)/float(b_len)) * similar(a, b, None), 
        similar(a, b, None),
        a_i,
        a, 
        b_i,
        b
    )

def similar_to_a_in_list(a_index, a_val, a_list, l):
    return max(
        map (
            lambda (b_i, b): elements_similarity(a_index, a_val, len(a_list), b_i, b, len(l)),
            enumerate(l)
        )
    )

def best_match_list(a, b):
    '''Every word in a returns an element link'''
    return [similar_to_a_in_list(i, tok, a, b) for (i, tok) in enumerate(a)]

def tagged_words_dict_with_all_matches(matches):
    '''Dict that appends all matches'''
    tagged_words = {}
    for m in matches:
        tagged_words[m[2]] = m[4]
        
    return tagged_words

def map_list_a_to_b(a, b):
    match_list = best_match_list(a, b)
    tagged_words = tagged_words_dict_with_all_matches(match_list)
    return tagged_words
