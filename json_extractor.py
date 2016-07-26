#!/usr/bin/enb python
import json
import itertools

def from_file_get_n_docs(file_path, doc_number=50):
    f = open(file_path)
    return [json.loads(l.strip()) for l in itertools.islice(f, doc_number)]

if __name__ == '__main__':
    docs = from_file_get_n_docs('./50_tagged_by_stanford.jsonl', 10)
    print docs
    print "Read {0} samples.".format(len(docs))



