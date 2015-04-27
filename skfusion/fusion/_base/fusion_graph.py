from collections import defaultdict, Iterable

from .fusion import DataFusionError


__all__ = ['FusionGraph']


class FusionGraph(object):
    """Container object for data sets and object types.

    Parameters
    ----------
    relations :

    Attributes
    ----------
    adjacency_matrix
    relations:
    object_types :
    """
    def __init__(self, relations=()):
        self.adjacency_matrix = defaultdict(lambda: defaultdict(list))
        self.relations = {}
        self.object_types = {}
        self.add(relations)

    def draw_graphviz(self, filename):
        """Draw the data fusion graph and save it to a file (SVG).

        Parameters
        ----------
        filename :
        """
        import pygraphviz as pgv
        fus_graph = pgv.AGraph(strict=False, directed=True)
        # object types
        for ot in self.object_types:
            fus_graph.add_node(ot.name)
        # relations
        ot2count = defaultdict(int)
        for relation in self.relations:
            ot1 = relation.row_type
            ot2 = relation.col_type
            ot2count[ot1, ot2] += 1
            if ot1 != ot2:
                label = '<<b>R</b><SUB>%s,%s</SUB><SUP>%d</SUP>' \
                        '<br/>>' % (ot1.name, ot2.name, ot2count[ot1, ot2])
                fus_graph.add_edge(ot1.name, ot2.name, text=label)
            else:
                label = '<<b>&Theta;</b><SUB>%s</SUB>' \
                        '<SUP>%d</SUP><br/>>' % (ot1.name, ot2count[ot1, ot2])
                fus_graph.add_edge(ot1.name, ot1.name, label=label)
        fus_graph.draw(filename, format='pdf', prog='dot')

    def add(self, relations):
        """Include a relation/constraint matrix into a fusion graph.

        Parameters
        ----------
        relations :
        """
        if not isinstance(relations, Iterable):
            relations = [relations]
        for relation in relations:
            self.relations[relation] = relation
            self.object_types[relation.row_type] = relation.row_type
            self.object_types[relation.col_type] = relation.col_type
            self.adjacency_matrix[relation.row_type][relation.col_type].append(relation)

    def get(self, row_type, col_type=None):
        """Return a relation matrix between two types of objects.

        Parameters
        ----------
        row_type : Object type identifier
        col_type : Object type identifies

        Returns
        -------
        relation :  generator
        """
        if row_type not in self.object_types:
            raise DataFusionError("Object types are not recognized.")
        if col_type is not None and col_type not in self.object_types:
            raise DataFusionError("Object types are not recognized.")
        for relation in self.adjacency_matrix[row_type][col_type]:
            yield relation
