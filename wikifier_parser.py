#!/usr/bin/env python
import copy
import json
from collections import defaultdict

from tagged_document_parsing_lib import type_mention, all_possible_mentions_for_surface_forms

wikifier_mention_surface_form = lambda m, words: u' '.join(words[m['wFrom'] : m['wTo'] + 1])

def wikifier_entity_surface_forms (e, words):
    return [wikifier_mention_surface_form(mention, words) for mention in e['support']]

def annotation_important_information(a):
    important_info = [
        'cosine', 'dbPediaIri', 'dbPediaTypes', 'secTitle',
        'secUrl', 'secLang'
    ]
    return {
        k: a.get(k, u'Not present') for k in important_info 
    }

def add_annotation_to_tagged_words_dict(a, d, words):
    for mention in a['support']:
        start = mention['wFrom']
        end = mention['wTo']
        for i in range(start, end + 1):
            d[i] = annotation_important_information(a)
            d[i]['start'] = start
            d[i]['end'] = end
            d[i]['wikifier-surface-form'] = wikifier_mention_surface_form(mention, words)
    return d

def parse_wikifier_doc(doc):
    annotation_dictionary = defaultdict(lambda: [])
    tagged_words = {}
    for a in doc['annotations']:
        surface_forms = wikifier_entity_surface_forms(a, doc['words'])
        mention_dicts = all_possible_mentions_for_surface_forms(surface_forms)
        
        types = [c['enLabel'] for c in a.get('wikiDataClasses', [])]
        title = a['title']
        
        if (len(types) > 0 and mention_dicts):
            for mention in mention_dicts:
                annotation_dictionary[json.dumps(mention, ensure_ascii=False)].append({
                    u'types': types,
                    u'title': title
                })
            tagged_words = add_annotation_to_tagged_words_dict(a, tagged_words, doc['words'])
                
    return {
        'entities': annotation_dictionary,
        'tagged-words': tagged_words,
        'tokens': doc['words']
    }

if __name__ == '__main__':
    from json_extractor import from_file_get_n_docs
    from pprint import PrettyPrinter

    wikifier_file_name = './100_tagged_by_wikifier.jsonl'
    wikifier_docs = from_file_get_n_docs(wikifier_file_name, 2)

    parsed_wikifier_docs = [parse_wikifier_doc(doc) for doc in wikifier_docs]

    pp = PrettyPrinter()
    pp.pprint(parsed_wikifier_docs[0])
