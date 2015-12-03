#!/usr/bin/env python


__author__ = 'Jamie Fujimoto'


# referenced code from http://www.bogotobogo.com/python/python_graph_data_structures.php


class Vertex(object):
    def __init__(self, node, label):
        self.id = node
        self.label = label
        self.edges = []


    def add_edge(self, neighbor_label, edge_label):
        edge = (self.label, neighbor_label, edge_label)
        self.edges.append(edge)


class Graph(object):
    def __init__(self, id):
        self.id = id
        self.vertices = {}


    def __iter__(self):
        return iter(self.vertices.values())


    def add_vertex(self, node, label=''):
        new_vertex = Vertex(node, label)
        self.vertices[node] = new_vertex


    def add_edge(self, node1, node2, label=''):
        if node1 not in self.vertices:
            self.add_vertex(node1)
        if node2 not in self.vertices:
            self.add_vertex(node2)
        self.vertices[node1].add_edge(self.vertices[node2].label, label)
        self.vertices[node2].add_edge(self.vertices[node1].label, label)


if __name__ == '__main__':
    g = Graph(1)

    g.add_vertex(10, 'a')
    g.add_vertex(20, 'b')
    g.add_vertex(30, 'a')
    g.add_vertex(40, 'b')

    g.add_edge(10, 20, '_')
    g.add_edge(10, 30, '_')
    g.add_edge(20, 30, '_')
    g.add_edge(30, 40, '_')

    print "id: {}".format(g.id)
    for v in g:
        print "{} {} {}".format(v.id, v.label, v.edges)