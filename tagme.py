#!/usr/bin/env python
from linkers_and_taggers import tagme_tag
import sample_data
import pprint

docs = sample_data.n_samples(50)
tagme_tags = tagme_tag(docs[0]['content'])

pp = pprint.PrettyPrinter()
pp.pprint(tagme_tags)
