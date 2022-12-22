import csv
import graphviz
import logging
from typing import Dict, List, Tuple
from collections import namedtuple, defaultdict

CSV_FILENAME = 'C:\\Users\\jabr9\\Downloads\\Stonetop Relationships - Stonetop NPCs.csv'
CSVRow = namedtuple('CSVRow',
                    ['color_hex', 'color_type', 'type', 'title', 'first_name', 'last_name', 'status', 'relation',
                     'relation_target', 'relation_back_ref'])
Relation = namedtuple('Relation', ['source', 'relation', 'target', 'back_ref'])

logging.getLogger().setLevel(logging.DEBUG)


class Coloring:
    _BY_TYPE = {}

    def __init__(self, hex_code, _type):
        self.hex_code = f"#{hex_code}"
        self.name = _type
        self._BY_TYPE[_type] = self

    @classmethod
    def for_name(cls, _type):
        return cls._BY_TYPE[_type].hex_code


class Node:

    def __init__(self, _type, title, first_name, last_name, status):
        self.type = _type
        self.title = title
        self.first_name = first_name
        self.last_name = last_name
        self.status = status

    def __repr__(self):
        return str(self.__dict__)

    @property
    def key(self):
        return self.first_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def display_name(self):
        title_display = f"\nthe {self.title}" if self.title else ''
        status_display = f"\n({self.status})" if self.status else ''
        return f"{self.first_name}{title_display}{status_display}"


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


def parse_rows(rows: List[CSVRow]) -> Tuple[Dict[str, Dict[str, Node]], List[Relation]]:
    nodes_by_type = defaultdict(dict)
    names, relations = set(), []
    for row in rows:
        if row.color_hex != '':  # there's a color type config
            Coloring(hex_code=row.color_hex, _type=row.color_type)

        if not row.first_name:
            logging.error(f"Row must ")

        node = Node(
            _type=row.type,
            title=row.title,
            first_name=row.first_name,
            last_name=row.last_name,
            status=row.status,
        )
        if node.first_name not in names:
            nodes_by_type[node.type][node.key] = node
            names.add(node.first_name)
            logging.debug(f"Added node {node}")
        else:
            existing = nodes_by_type[node.type][node.key]
            if existing.full_name != node.full_name:
                logging.error(f"")

        if row.relation and row.relation_target:
            relation = Relation(
                source=row.first_name,
                relation=row.relation,
                target=row.relation_target,
                back_ref=row.relation_back_ref
            )
            relations.append(relation)
            logging.debug(f"Added relation {relation}")
        elif row.relation or row.relation_target or row.relation_back_ref:
            logging.error(f"Problem with relation in row {row}")

    return nodes_by_type, relations


def create_graph(nodes_by_type: Dict[str, Dict[str, Node]], relations: List[Relation]) -> str:
    dot = graphviz.Digraph(name='Relations', format='png')

    for _type, node_map in nodes_by_type.items():
        with dot.subgraph(name=_type) as s:
            s.node_attr.update(style='filled', fillcolor=Coloring.for_name(_type))
            for n in node_map.values():
                s.node(name=n.first_name, label=n.display_name)

    for r in relations:
        dot.edge(r.source, r.target, label=r.relation)

    return dot.render(directory='output')


if __name__ == '__main__':
    import sys
    file = sys.argv[1] if len(sys.argv) > 1 else CSV_FILENAME
    png_file = create_graph(*parse_rows(load_csv(file)))
    logging.info(f"Graph saved to {png_file}")
