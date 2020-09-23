import os
import argparse
import sys

from src import database
from src import parser
from src import utils

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--query', required=True)

    parser.add_argument('--type',
        choices=['tree', 'vector'], required='--query' in sys.argv)

    args = parser.parse_args()

    return args

def main(args):
    db = database.Database(os.path.abspath('database.ini'))
    query = utils.read_query(args.query)
    plan = db.explain_query(query)

    if args.type == 'tree':
        tree = parser.build_tree(plan[0][0]["Plan"])
        print(tree)
    elif args.type == 'vector':
        vector = parser.build_vector(plan[0][0]["Plan"])
        print(vector)
    else:
        print("Invalid arguments. Run 'python main.py --help'")

    db.close()

if __name__ == '__main__':
    args = get_args()
    main(args)
