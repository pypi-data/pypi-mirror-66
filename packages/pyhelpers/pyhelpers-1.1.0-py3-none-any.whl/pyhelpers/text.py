""" Text-related """

import re


# Find similar string from a list of strings
def find_similar_str(x, lookup_list, processor='fuzzywuzzy', **kwargs):
    """
    :param x: [str]
    :param lookup_list: [iterable]
    :param processor: [str] (default: 'fuzzywuzzy')
    :param substitution_cost: [int] (default: 100)
    :return: [str]
    """
    assert processor in ('fuzzywuzzy', 'nltk'), '\"processor\" must be either \"fuzzywuzzy\" or \"nltk\".'

    if processor == 'fuzzywuzzy':
        import fuzzywuzzy.fuzz
        l_distances = [fuzzywuzzy.fuzz.token_set_ratio(x, a, **kwargs) for a in lookup_list]
        the_one = lookup_list[l_distances.index(max(l_distances))] if l_distances else None

    elif processor == 'nltk':
        import nltk.metrics
        l_distances = [nltk.edit_distance(x, a, **kwargs) for a in lookup_list]
        the_one = lookup_list[l_distances.index(min(l_distances))] if l_distances else None

    else:
        the_one = None

    return the_one


# Find from a list the closest, case-insensitive, str to the given one
def find_matched_str(x, lookup_list):
    """
    :param x: [str; None] (if None, return None)
    :param lookup_list: [iterable]
    :return: [str; list; None]
    """
    # assert isinstance(x, str), "'x' must be a string."
    # assert isinstance(lookup, list) or isinstance(lookup, tuple), "'lookup' must be a list/tuple"
    if x == '' or x is None:
        return None
    else:
        for y in lookup_list:
            if re.match(x, y, re.IGNORECASE):
                return y


# Convert compressed sparse matrix to a dictionary
def csr_matrix_to_dict(csr_matrix, vectorizer):
    features = vectorizer.get_feature_names()
    dict_data = []
    for i in range(len(csr_matrix.indptr) - 1):
        sid, eid = csr_matrix.indptr[i: i + 2]
        row_feat = [features[x] for x in csr_matrix.indices[sid:eid]]
        row_data = csr_matrix.data[sid:eid]
        dict_data.append(dict(zip(row_feat, row_data)))

    import pandas as pd
    mat_dict = pd.Series(dict_data).to_frame('word_count')

    return mat_dict
