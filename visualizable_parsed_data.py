#!/usr/bin/env python
import json
import sys
import logging

from visualizer_preprocessor import tag_tokens_with_linked_doc

from json_extractor import from_file_get_n_docs

FILENAMES = {
    'stanford': '100_parsed_from_stanford.jsonl',
    'wikifier': '100_parsed_from_wikifier.jsonl',
    'tagme'   : '100_parsed_from_tagme.jsonl'
}

def common_tag_docs(tagger, n=50, color="royalblue"):
    filename = FILENAMES.get(tagger, None)
    if filename:
        docs = from_file_get_n_docs(filename, n)
        stanford_docs = from_file_get_n_docs(FILENAMES['stanford'], n)
        tokens = [doc['tokens'] for doc in stanford_docs]

        logging.info('Parsing {0} docs...'.format(n))
        parsed_docs = map(
            lambda (i, doc): tag_tokens_with_linked_doc(tokens[i], doc, color),
            enumerate(docs)
        )
        logging.info('Converting to json...')
        json_docs   = map(lambda d: json.dumps(d['colored-tagged-words'], ensure_ascii='False'), parsed_docs)

        logging.info('Output the json docs...')
        for i, doc in enumerate(json_docs):
            logging.info('Printing file {0}.\n{1}\n'.format(i, doc))
            print doc
    else:
        logging.warning('Must specify an existing tagger!')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    tagger = sys.argv[1] if len(sys.argv) > 0 else None
    n = sys.argv[2] if len(sys.argv) > 1 else None
    color = sys.argv[3] if len(sys.argv) > 2 else "royalblue"

    if (tagger and n):
        common_tag_docs(tagger, int(n), color)



    
