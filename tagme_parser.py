#!/usr/bin/env python
import copy
import json
from collections import defaultdict

from tagged_document_parsing_lib import generate_mentions_for_surface_form

def parse_tagme_doc(doc):
    indexed_tagme_annotations = defaultdict(lambda: [])
    parsed_doc = {}
    parsed_doc[u'tokens'] = []
    parsed_doc[u'tagged-words'] = {}
    for i, annotation in enumerate(doc['annotations']):
        all_possible_annotation_indexes = generate_mentions_for_surface_form(annotation['spot'])

        tokens = annotation['spot'].split()
        start = len(parsed_doc[u'tokens'])
        end = start + len(tokens) - 1

        annotation[u'start'] = start
        annotation[u'end'] = end

        for index in all_possible_annotation_indexes:
            indexed_tagme_annotations[json.dumps(index, ensure_ascii=False)].append(annotation)
            
        for tok in tokens:
            parsed_doc[u'tagged-words'][len(parsed_doc[u'tokens'])] = copy.deepcopy(annotation)
            parsed_doc[u'tokens'].append(tok)
            
    parsed_doc[u'entities'] = indexed_tagme_annotations

    return parsed_doc

if __name__ == '__main__':
    from json_extractor import from_file_get_n_docs
    from pprint import PrettyPrinter

    tagme_file_name = './100_tagged_by_tagme_longtext_0_epsilon_dot1_includecategories_includeallspots.jsonl'
    tagme_docs = from_file_get_n_docs(tagme_file_name, 2)

    parsed_tagme_docs = [parse_tagme_doc(doc) for doc in tagme_docs]

    pp = PrettyPrinter()
    pp.pprint(parsed_tagme_docs[0])
