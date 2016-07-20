#!/usr/bin/env python
from linkers_and_taggers import wikifier_tag
import sample_data
import pprint

docs = sample_data.n_samples(50)
wikifier_tags = wikifier_tag(docs[0]['content'])

pp = pprint.PrettyPrinter()
pp.pprint(wikifier_tags)
