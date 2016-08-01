#!/usr/bin/env python
import json
import itertools

def n_samples(sample_number=50):
    f = open('../signalmedia-1m.jsonl')
    return [json.loads(l.strip()) for l in itertools.islice(f, sample_number)]


if __name__ == '__main__':
    samples = n_samples()
    print samples
    print "Read {0} samples.".format(len(samples))



