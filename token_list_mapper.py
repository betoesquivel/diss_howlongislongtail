#!/usr/bin/env python
from similarity import similar, find_similar_to_a_in_dict_b, a_is_not_in_dict_b, compare_linkers_parsed_docs

valid_index = lambda i, arr: i < len(arr)

def should_shift_list (arr, i, shifts, max_shifts, previous_similar):
    return valid_index(i+shifts, arr) and shifts <= max_shifts and not previous_similar

def compare_a_to_b_shifting_max_from_indexes (a, b, max_shifts, a_i, b_i):
    
    next_shift = 0
    current_shift = 0
    are_similar = False
    while should_shift_list(a, a_i, next_shift, max_shifts, are_similar):
        are_similar = similar(a[a_i + next_shift], b[b_i], 0.6)
        current_shift = next_shift
        next_shift += 1    
    
    current_shift = -1 if not are_similar else current_shift
    return current_shift

def shift_indexes(a_i, b_i, a_shifts, b_shifts):
    if a_shifts > 0 and b_shifts > 0:
        if a_shifts <= b_shifts:
            a_i += a_shifts
        else:
            b_i += b_shifts
    elif a_shifts > 0:
        a_i += a_shifts
    else:
        b_i += b_shifts
    
    return a_i, b_i

def update_max_shifts(max_shifts, a_shifts, b_shifts):
    return max_shifts - max([a_shifts, b_shifts])

def map_token_list_a_to_b(a, b):
    max_shifts = abs(len(a) - len(b)) + 1
    a_index = 0
    b_index = 0
    
    mapping = {}
    still_similar = True
    while (a_index < len(a) or b_index < len(b) and still_similar):
        
        a_index = a_index if a_index < len(a) else len(a) - 1
        b_index = b_index if b_index < len(b) else len(b) - 1
        
        a_shifts = compare_a_to_b_shifting_max_from_indexes(a, b, max_shifts, a_index, b_index)
        b_shifts = compare_a_to_b_shifting_max_from_indexes(b, a, max_shifts, b_index, a_index)
        
        if a_shifts == -1 and b_shifts == -1:
            still_similar = False
        else:
            a_index, b_index = shift_indexes(a_index, b_index, a_shifts, b_shifts)
            max_shifts = update_max_shifts(max_shifts, a_shifts, b_shifts)
            mapping[a_index] = b_index
        
        a_index += 1
        b_index += 1
    
    return mapping

if __name__ == '__main__':
    a = [u'aaaa', u'a.', u'hola', u'..', u',', u'perro']
    b = [u"aaaa's", u'!!!', u'a', u'hola!!', u'perro']
     
    print map_token_list_a_to_b(a, b)
