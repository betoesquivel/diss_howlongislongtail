#!/usr/bin/env python
from linkers_and_taggers import stanford_tag, stanford_tagger
import sample_data
import pprint

docs = sample_data.n_samples(50)
stanford_tags = stanford_tag(docs[0]['content'], stanford_tagger())

pp = pprint.PrettyPrinter()
pp.pprint(stanford_tags)
