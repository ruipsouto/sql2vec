import json
from collections import Counter

from nested_lookup import nested_lookup

def encoder(node):
    """
    Returns an encoded node as a list of tuples.
    """
    codec = ['Aggregate', 'Merge Join', 'Sort', 'Nested Loop', 'Seq Scan',
        'Index Scan','null']

    arr = [int(codec[i] in node) for i, _ in enumerate(codec)]
    arr += node[-2:]

    return [tuple(arr)]

def build_tree(json, lookup_keys = ["Node Type", "Plan Rows", "Total Cost"]):
    if isinstance(json, dict):
        null = tuple(encoder(["null", 0, 0.0]))
        node = []
        node.extend(encoder([json.get(item) for item in lookup_keys]))

        if "Plans" in json:
            node.append(build_tree(json["Plans"][0], lookup_keys))
            if len(json["Plans"]) > 1:
                node.append(build_tree(json["Plans"][1], lookup_keys))
            else:
                node.append(null)
        return tuple(node)

    elif isinstance(json, list):
        for item in json:
            build_tree(item, lookup_keys)

def beautify(tree, level=0):
    ret = "\t" * level + str(tree[0]) + "\n"
    if len(tree) is not 1:
        ret += beautify(tree[1], level+1)
        ret += beautify(tree[2], level+1)
    return ret

def build_vector(json):
    operators = nested_lookup('Node Type', json)
    cost = json['Total Cost']
    rows = json['Plan Rows']

    codec = ['Aggregate', 'Merge Join', 'Sort', 'Nested Loop', 'Seq Scan',
        'Index Scan']

    arr = [Counter(operators)[c] for c in codec]
    arr.append(rows)
    arr.append(cost)

    return arr
