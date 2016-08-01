#!/usr/bin/env python
similar = lambda a, b, r=0.95: SequenceMatcher(None, a.lower(), b.lower()).ratio() >= r
find_similar_to_a_in_dict_b = lambda a, b, r=0.95: [b_key for b_key in b if similar(a, b_key, r)]
a_is_not_in_dict_b = lambda a, b, r=0.95: not find_similar_to_a_in_dict_b(a, b, r)
compare_linkers_parsed_docs = lambda a, b, n, r=0.95: [(i, a_entity) for (i, (a_doc, b_doc)) in enumerate(zip(a[0:n], b[0:n])) for a_entity in a_doc['entities'] if a_is_not_in_dict_b(a_entity, b_doc, r)]
