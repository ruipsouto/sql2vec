import os
import time

def read_query(filename):
    print('Reading query from {}...'.format(filename))

    with open(filename, 'r') as f:
        query = f.read()

    return query
