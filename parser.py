#!/usr/bin/env python
import json
import sys
import logging

from stanford_parser import parse_stanford_doc
from wikifier_parser import parse_wikifier_doc
from tagme_parser    import parse_tagme_doc

from json_extractor import from_file_get_n_docs

FILENAMES = {
    'stanford': '100_tagged_by_stanford.jsonl',
    'wikifier': '100_tagged_by_wikifier.jsonl',
    'tagme'   : '100_tagged_by_tagme_longtext_0_epsilon_dot1_includecategories_includeallspots.jsonl'
}

PARSERS = {
    'stanford': parse_stanford_doc,
    'wikifier': parse_wikifier_doc,
    'tagme'   : parse_tagme_doc
}

def parse_tagger_docs(tagger, n=50):
    filename = FILENAMES.get(tagger, None)
    parse    = PARSERS.get(tagger, None)
    if filename and parse:
        docs = from_file_get_n_docs(filename, n)

        logging.info('Parsing {0} docs...'.format(n))
        parsed_docs = map(parse, docs)
        logging.info('Converting to json...')
        json_docs   = map(lambda d: json.dumps(d, ensure_ascii='False'), parsed_docs)

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

    if (tagger and n):
        parse_tagger_docs(tagger, int(n))



    
