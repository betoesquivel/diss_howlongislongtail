#!/usr/bin/env python
from similarity import map_list_a_to_b
from collections import defaultdict
import copy

def merge_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    
    return z

add_color_to_map = lambda c, m: {int(k): merge_dicts({'color': c}, v) for k, v in m.items()}

no_match_color = {'color': 'white'}
word_tag_from_index_and_maps = lambda i, atob, b: b.get(atob[i], no_match_color)

def tag_tokens_with_linked_doc(tokens, linker_doc, color="royalblue"):
    tokens_to_linker = map_list_a_to_b(tokens, linker_doc['tokens'])
    
    tagged_words = add_color_to_map(color, linker_doc['tagged-words'])
    tags = [word_tag_from_index_and_maps(i, tokens_to_linker, tagged_words) for (i, word) in enumerate(tokens)]
    
    doc = copy.deepcopy(linker_doc)
    doc['colored-tagged-words'] = tags
    doc['colored-tokens'] = tokens

    return doc

if (__name__ == '__main__'):
    from json_extractor import from_file_get_n_docs
    import json
    STANFORD_FILENAME = '100_parsed_from_stanford.jsonl'
    WIKIFIER_FILENAME = '100_parsed_from_wikifier.jsonl'
    TAGME_FILENAME    = '100_parsed_from_tagme.jsonl'

    stanford_parsed_docs = from_file_get_n_docs(STANFORD_FILENAME, 5)
    wikifier_parsed_docs = from_file_get_n_docs(WIKIFIER_FILENAME, 5)
    tagme_parsed_docs = from_file_get_n_docs(TAGME_FILENAME, 5)

    test_index = 0
    stanford_doc = stanford_parsed_docs[test_index]
    wikifier_doc = wikifier_parsed_docs[test_index]
    tagme_doc = tagme_parsed_docs[test_index]

    stanford_to_wikifier = tag_tokens_with_linked_doc(stanford_doc['tokens'], wikifier_doc)['colored-tagged-words']
    stanford_to_tagme = tag_tokens_with_linked_doc(stanford_doc['tokens'], tagme_doc, "tomato")['colored-tagged-words']

    token        = stanford_doc['tokens'][2]
    wikifier_tag = stanford_to_wikifier  [2]
    tagme_tag    = stanford_to_tagme     [2]

    print "Tags for word {0}\n".format(token)
    print "WIKIFIER\n{0}\n\nTAMGE{1}\n".format(json.dumps(wikifier_tag), json.dumps(tagme_tag))


