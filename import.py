import csv
import logging
from collections import namedtuple, defaultdict
from typing import Dict, List, Tuple

import graphviz

CSV_FILENAME = 'C:\\Users\\jabr9\\Downloads\\Stonetop Relationships - Stonetop NPCs.csv'
CSVRow = namedtuple('CSVRow',
                    ['type', 'title', 'first_name', 'last_name', 'status', 'relation',
                     'relation_target', 'relation_back_ref', 'mutual'])
logging.getLogger().setLevel(logging.DEBUG)

def load_csv(filename) -> List[CSVRow]:
    ret = []
    with open(filename) as f:
        reader = csv.reader(f)
        for i, r in enumerate(reader):
            if i == 0:
                # skip header
                continue
            ret.append(CSVRow(*r))
    return ret

def parse_rows(rows: List[CSVRow]) -> None:
    nodes_by_type = defaultdict(dict)
    names, relations = set(), []
    for row in rows:

    return nodes_by_type, relations


def create_graph(nodes_by_type: Dict[str, Dict[str, Node]], relations: List[Relation]) -> str:
    dot = graphviz.Digraph(name='Relations', format='png')

    return dot.render(directory='output')


if __name__ == '__main__':
    import sys

    file = sys.argv[1] if len(sys.argv) > 1 else CSV_FILENAME
    png_file = create_graph(*parse_rows(load_csv(file)))
    logging.info(f"Graph saved to {png_file}")
