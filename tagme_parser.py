#!/usr/bin/env python
import copy
import json
from collections import defaultdict

from tagged_document_parsing_lib import generate_mentions_for_surface_form

def parse_tagme_doc(doc):
    indexed_tagme_annotations = defaultdict(lambda: [])
    parsed_doc = {}
    parsed_doc[u'tagged-words'] = {}
    
    raw_text = doc['raw']
    parsed_doc[u'tokens'] = raw_text.split()

    for i, annotation in enumerate(doc['annotations']):
        all_possible_annotation_indexes = generate_mentions_for_surface_form(annotation['spot'])

        surface_form = annotation['spot']
        
        start_word_index = raw_text[:annotation['start']].split().__len__()
        end_word_index = start_word_index + len(surface_form.split())

        annotation[u'start'] = start_word_index
        annotation[u'end'] = end_word_index - 1

        for index in all_possible_annotation_indexes:
            indexed_tagme_annotations[json.dumps(index, ensure_ascii=False)].append(annotation)
            
        for i in range(start_word_index, end_word_index):
            parsed_doc[u'tagged-words'][i] = copy.deepcopy(annotation)
            
    parsed_doc[u'entities'] = indexed_tagme_annotations
    
    return parsed_doc

if __name__ == '__main__':
    from json_extractor import from_file_get_n_docs
    from pprint import PrettyPrinter

    tagme_file_name = './100_tagged_by_tagme_with_raw_longtext_0_epsilon_dot1_includecategories_includeallspots.jsonl'
    tagme_docs = from_file_get_n_docs(tagme_file_name, 2)

    parsed_tagme_docs = [parse_tagme_doc(doc) for doc in tagme_docs]

    pp = PrettyPrinter()
    pp.pprint(parsed_tagme_docs[0])
