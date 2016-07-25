#!/usr/bin/env python
import os
import requests
import json
import pandas as pd
from nltk.tag import StanfordNERTagger

# Environment information and setup
TAGME_KEY = os.environ['TAGME_KEY']
WIKIFIER_KEY = os.environ['WIKIFIER_KEY']
STANFORD_JARS = os.environ['STANFORD_JARS']
os.environ['CLASSPATH'] = STANFORD_JARS

# ENDPOINTS
WIKIFIER_URL  = "http://www.wikifier.org/annotate-article"
TAGME_URL = "https://tagme.d4science.org/tagme/tag"

def json_foolproof_loads(text):
    try:
        return json.loads(text)
    except:
        return {}

# TAGME
# Usage: tagme_tag(text)
tagme_payload = lambda text: {
    'text': text,
    'lang': 'en',
    'gcube-token': TAGME_KEY
}
tagme_call = lambda text: requests.get(TAGME_URL, params=tagme_payload(text))
tagme_tag = lambda text: json_foolproof_loads(tagme_call(text).text).get('annotations', [])

# WIKIFIER
# Usage: wikifier_tag(text)
wikifier_payload = lambda text: {
    'text': text,
    'lang': 'en',
    'userKey': WIKIFIER_KEY
}
wikifier_call = lambda text: requests.get(WIKIFIER_URL, params=wikifier_payload(text))
wikifier_tag = lambda text: json_foolproof_loads(wikifier_call(text).text).get('annotations', [])

# STANFORD NER
# Usage:
#  stanford_tagger() => <StanfordNERTagger>
#  stanford_tag(text, <StanfordNERTagger>)
#  Therefore:
#   stanford_tag(text, stanford_tagger())
stanford_tagger = lambda: StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')
stanford_tag = lambda text, tagger: tagger.tag(text.split())


if __name__ == '__main__':
    import sample_data
    import pprint
    docs = sample_data.n_samples(50)
    tagme_tags = tagme_tag(docs[2]['content'])
    wikifier_tags = wikifier_tag(docs[2]['content'])
    stanford_tags = stanford_tag(docs[2]['content'], stanford_tagger())
    pp = pprint.PrettyPrinter()
    pp.pprint(wikifier_tags)
    pp.pprint(stanford_tags)
    pp.pprint(tagme_tags)

