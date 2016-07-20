#!/usr/bin/env python
from linkers_and_taggers import wikifier_tag
import sample_data
import pprint
import sys
import json

docs = sample_data.n_samples(int(sys.argv[1]) if len(sys.argv) > 1 else None)
json_docs = [json.dumps(wikifier_tag(doc['content'])) for doc in docs]

for doc in json_docs:
    print doc

#wikifier_tags = wikifier_tag(docs[0]['content'])
#pp = pprint.PrettyPrinter()
#pp.pprint(wikifier_tags)
