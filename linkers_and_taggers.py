#!/usr/bin/env python
import os
import requests
import json
import pandas as pd
from nltk.tag import StanfordNERTagger

# Environment information and setup
TAGME_KEY = os.environ['TAGME_KEY']
WIKIFIER_KEY = os.environ['WIKIFIER_KEY']
STANFORD_JARS = os.environ.get('STANFORD_JARS')
os.environ['CLASSPATH'] = STANFORD_JARS

# ENDPOINTS
WIKIFIER_URL  = "http://www.wikifier.org/annotate-article"
TAGME_URL = "https://tagme.d4science.org/tagme/tag"

# TAGME
# Usage: tagme_tag(text)
tagme_payload = lambda text: {
    'text': text,
    'lang': 'en',
    'gcube-token': TAGME_KEY
}
tagme_call = lambda text: requests.get(TAGME_URL, params=tagme_payload(text))
tagme_tag = lambda text: json.loads(tagme_call(text).text).get('annotations', [])

# WIKIFIER
# Usage: wikifier_tag(text)
wikifier_payload = lambda text: {
    'text': text,
    'lang': 'en',
    'userKey': WIKIFIER_KEY
}
wikifier_call = lambda text: requests.get(WIKIFIER_URL, params=wikifier_payload(text))
wikifier_tag = lambda text: json.loads(wikifier_call(text).text).get('annotations', [])

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
    docs = sample_data.n_samples(50)
    tagme_tag(docs[0]['content'])
    wikifier_tag(docs[0]['content'])
    stanford_tag(docs[0]['content'], stanford_tagger())
