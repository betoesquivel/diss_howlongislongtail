#!/usr/bin/env python
from linkers_and_taggers import tagme_tag
import sample_data
import pprint
import sys
import json

docs = sample_data.n_samples(int(sys.argv[1]) if len(sys.argv) > 1 else None)
json_docs = [json.dumps(tagme_tag(doc['content'])) for doc in docs]

for doc in json_docs:
    print doc

#tagme_tags = tagme_tag(docs[0]['content'])
#pp = pprint.PrettyPrinter()
#pp.pprint(tagme_tags)
