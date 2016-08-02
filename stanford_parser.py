#!/usr/bin/env python
from collections import defaultdict
import json

starts_new_entity = lambda prev, curr: prev != curr and curr != 'O'
is_in_entity = lambda prev, curr: prev == curr and curr != 'O'
is_outside_entity = lambda prev, curr: prev != curr and curr == 'O'

def parse_stanford_doc(doc):
    previous_type = u'O'
    start_word = 0
    end_word = 0
    surface_form = u''
    type_counts = defaultdict(lambda: 0)
    
    document = {}
    document[u'entities'] = defaultdict(lambda: {'counts': 0, 'mentions': []})
    document[u'tagged-words'] = {}
    document[u'tokens'] = []
    for i, [w, t] in enumerate(doc):

        document[u'tokens'].append(w)

        if starts_new_entity(previous_type, t):
            start_word = i
            end_word = i
            surface_form = w
        elif is_in_entity(previous_type, t):
            end_word = i
            surface_form += u" {0}".format(w)
        elif is_outside_entity(previous_type, t):
            mention = {
                u'surface-form': surface_form,
                u'type': previous_type,
            }
            json_mention = json.dumps(mention, ensure_ascii=False)

            type_counts[previous_type+u'_M'] += 1
            type_counts[previous_type+u'_E'] += 1 if json_mention not in document['entities'] else 0
            
            document['entities'][json_mention]['counts'] += 1
            document['entities'][json_mention]['mentions'].append({
                'start' : start_word,
                'end' : end_word
            })
            
            mention['start'] = start_word
            mention['end'] = end_word 
            for i in range(start_word, end_word + 1):
                document[u'tagged-words'][i] = mention
            
            surface_form = u''
            
        previous_type = t
    
    document['ORG_MENTIONS'] = type_counts['ORGANIZATION_M']
    document['LOC_MENTIONS'] = type_counts['LOCATION_M']
    document['PER_MENTIONS'] = type_counts['PERSON_M']
    document['ORG_ENTITIES'] = type_counts['ORGANIZATION_E']
    document['LOC_ENTITIES'] = type_counts['LOCATION_E']
    document['PER_ENTITIES'] = type_counts['PERSON_E']
    return document

if __name__ == '__main__':
    from json_extractor import from_file_get_n_docs
    from pprint import PrettyPrinter

    stanford_file_name = './50_tagged_by_stanford.jsonl'
    
    stanford_docs = from_file_get_n_docs(stanford_file_name, 2)
    stanford_parsed_docs = [parse_stanford_doc(doc) for doc in stanford_docs]

    pp = PrettyPrinter()
    pp.pprint(stanford_parsed_docs[0])
