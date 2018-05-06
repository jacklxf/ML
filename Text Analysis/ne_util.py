import nltk

def extract_ne_from_tree ( tree ):
    result = []
    for s in tree.subtrees():
        label = s.label()
        if (label == 'PERSON' or label == 'ORGANIZATION' or label == 'GPE'):
            leaves = s.leaves()
            ne = ''
            for l in leaves:
                ne = ne + ' ' + l[0]
            result.append((label, ne[1:]))
    return result