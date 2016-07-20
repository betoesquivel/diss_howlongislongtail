#!/usr/bin/env python
from linkers_and_taggers import stanford_tag, stanford_tagger
import sample_data
import pprint
import sys
import json

docs = sample_data.n_samples(int(sys.argv[1]) if len(sys.argv) > 1 else None)
tagger = stanford_tagger()
json_docs = [json.dumps(stanford_tag(doc['content'], tagger)) for doc in docs]

for doc in json_docs:
    print doc

#stanford_tags = stanford_tag(docs[0]['content'], stanford_tagger())
#pp = pprint.PrettyPrinter()
#pp.pprint(stanford_tags)
