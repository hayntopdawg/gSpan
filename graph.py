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
    def __init__(self):
        self.id = None
        self.vertices = {}


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