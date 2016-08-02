#!/usr/bin/env python
import copy

def type_mention(mention_type, mention):
    mention[u'type'] = mention_type
    return copy.deepcopy(mention)

def generate_mentions_for_surface_form (surface_form):
    mentions = []
    mention = {u'surface_form': surface_form}
    
    types = [u'ORGANIZATION', u'LOCATION', u'PERSON']
    
    mentions.extend([type_mention(t, mention) for t in types ])

    return mentions

extend_reducer = lambda l1, l2: l1.extend(l2) if l1 else l2

def flatten(list):
    flat = []
    map(flat.extend, list)

    return flat

def all_possible_mentions_for_surface_forms(sfs):
    mentions = flatten(map(generate_mentions_for_surface_form, sfs))
    
    return mentions
