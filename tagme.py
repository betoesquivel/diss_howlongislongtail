#!/usr/bin/env python
from linkers_and_taggers import tagme_tag
import sample_data
import pprint
import sys
import json
import time

docs = sample_data.n_samples(int(sys.argv[1]) if len(sys.argv) > 1 else None)

json_docs = []
for i, doc in enumerate(docs):
    json_docs.append(json.dumps(tagme_tag(doc['content'][:5000])))

# print "Tagging doc {0} of 10.".format(3)
# doc = docs[3]
# json_docs.append(json.dumps(tagme_tag(doc['content'][:5000])))

for doc in json_docs:
    print doc

#tagme_tags = tagme_tag(docs[0]['content'])
#pp = pprint.PrettyPrinter()
#pp.pprint(tagme_tags)
