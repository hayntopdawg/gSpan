#!/usr/bin/env python

__author__ = 'Jamie Fujimoto'

# referenced code from http://www.bogotobogo.com/python/python_graph_data_structures.php


class Vertex(object):
    def __init__(self, id, label):
        self.id = id
        self.label = label
        self.neighbors = []
        self.edges = []


    def add_edge(self, neighbor, neighbor_label, edge_label):
        self.neighbors.append(neighbor)
        edge = (self.label, neighbor_label, edge_label)  # might be an issue because it does not maintain vertex IDs
        self.edges.append(edge)


class Graph(object):
    def __init__(self, id):
        self.id = id
        self.vertices = {}


    def __iter__(self):
        return iter(self.vertices.values())


    def add_vertex(self, v_id, label=''):
        new_vertex = Vertex(v_id, label)
        self.vertices[v_id] = new_vertex


    def add_connection(self, node1, node2, label=''):
        if node1 not in self.vertices:
            self.add_vertex(node1)
        if node2 not in self.vertices:
            self.add_vertex(node2)
        self.vertices[node1].add_connection(node2, self.vertices[node2].label, label)
        self.vertices[node2].add_connection(node1, self.vertices[node1].label, label)


    def add_ext(self, t):
        node1, node2, node1_label, node2_label, edge_label = t
        self.add_vertex(node1, node1_label)
        self.add_vertex(node2, node2_label)
        self.add_connection(node1, node2, edge_label)


    def get_distinct_label_tuples(self):
        tuples = []
        for v in self.vertices.values():
            tuples.extend(v.edges)
        distinct = list(set(tuples))
        distinct.sort()
        return distinct


    def get_vertex_by_label(self, label):
        return [v.id for v in self.vertices.values() if v.label == label]


    def get_neighbors(self, v_id):
        return self.vertices[v_id].neighbors


if __name__ == '__main__':
    g = Graph(1)

    g.add_vertex(10, 'a')
    g.add_vertex(20, 'b')
    g.add_vertex(30, 'a')
    g.add_vertex(40, 'b')

    g.add_connection(10, 20, '_')
    g.add_connection(10, 30, '_')
    g.add_connection(20, 30, '_')
    g.add_connection(30, 40, '_')

    print "id: {}".format(g.id)
    for v in g:
        print "{} {} {}".format(v.id, v.label, v.edges)
    print ""
    # print g.get_vertex_by_label('a')  # Test get_vertex_by_label
    # print g.get_distinct_label_tuples()  # Test get_distinct_label_tuples

    # # Test add_ext
    # code1 = (0, 1, 'a', 'a', '_')
    # code2 = (1, 2, 'b', 'a', '_')
    # g.add_ext(code1)
    # g.add_ext(code2)
    # print "id: {}".format(g.id)
    # for v in g:
    #     print "{} {} {}".format(v.id, v.label, v.edges)
    # print g.get_distinct_label_tuples()