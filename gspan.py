#!/usr/bin/env python

import copy
import graph
import graph_reader


__author__ = 'Jamie Fujimoto'


num_call = 1


def build_graph(C):
    """ Builds a graph using code C. """

    g = graph.Graph(1)
    for t in C:
        g.add_ext(t)
    return g


def sub_graph_isomorphisms(C, G):
    """ Returns all of the possible isomorphisms for code C in graph G. """

    phi = [[x] for x in G.get_vertex_by_label(C[0][2])]
    for t in C:
        u, v, u_label, v_label, edge_label = t
        phi_prime = []
        for p in phi:
            if v > u:
                # forward edge
                for x in G.get_neighbors(p[u]):
                    if (x not in p) and \
                       (G.get_vertex_label(x) == v_label) and \
                       (G.get_edge_label(p[u], x) == edge_label):
                        p_prime = p + [x]
                        phi_prime.append(p_prime)
            else:
                # backward edge
                if p[v] in G.get_neighbors(p[u]):
                    phi_prime.append(p)
        phi = copy.copy(phi_prime)
    return copy.copy(phi)


def right_most_path_extensions(C, D):
    """ Returns all possible extensions for the right most path with their respective supports. """

    Gc = build_graph(C)
    R = [v.id for v in Gc]  # nodes on the rightmost path in C
    if R:
        u_r = R[-1]  # rightmost child in C (DFS number)
    else:
        u_r = 0
    E = {}  # set of extensions from C

    for G in D:
        E[G.id] = []
        if not C:
            # add distinct label tuples in Gi as forward extensions
            for dist_tuple in G.get_distinct_label_tuples():
                E[G.id].append((0, 1) + dist_tuple)
        else:
            phi = sub_graph_isomorphisms(C, G)
            for p in phi:  # for each isomorphism in phi
                # backward extensions from rightmost child
                for x in G.get_neighbors(p[u_r]):
                    vs = Gc.get_vertex_by_label(G.get_vertex_label(x))
                    valid_v = [v for v in vs if (p[v] == x) and (v in R) and ((u_r, v) not in Gc.connections)]
                    for v in valid_v:
                        b = (u_r, v, Gc.get_vertex_label(u_r), Gc.get_vertex_label(v), G.get_edge_label(p[u_r], p[v]))
                        E[G.id].append(b)

                # forward extension from nodes on rightmost path
                for u in R:
                    neigbors = [n for n in G.get_neighbors(p[u]) if n not in p]
                    for x in neigbors:
                        E[G.id].append((u, u_r + 1,
                                        Gc.get_vertex_label(u),
                                        G.get_vertex_label(x),
                                        G.get_edge_label(p[u], x)))

    # compute the support of each extension
    sup = {}
    for G in E:
        distinct_exts = list(set(E[G]))  # make each list of tuples distinct
        for ext in distinct_exts:
            if ext not in sup:
                sup[ext] = 1
            else:
                sup[ext] += 1
    sorted_tuples = sort_tuples(sup.items())
    return sorted_tuples


def sort_tuples(E):
    sorted_E = []
    while len(E) > 0:
        min_tuple = find_min_edge(E)
        sorted_E.append(min_tuple)
        E.remove(min_tuple)
    return copy.copy(sorted_E)


def find_min_edge(E):
    min_edge, min_edge_sup = [], 0
    for (edge, sup) in E:
        if not min_edge:
            min_edge, min_edge_sup = edge, sup
        else:
            # if edge is smaller than min_edge
            if is_smaller(edge, min_edge):
                min_edge, min_edge_sup = edge, sup
    return min_edge, min_edge_sup


def is_smaller(s, t):
    # (i, j) = (x, y)
    if s[0] == t[0] and s[1] == t[1]:
        if s < t:
            return True
        else:
            return False
    else:
        # Condition 1 (Both forward edges)
        if s[0] < s[1] and t[0] < t[1]:
            # (a) j < y
            if s[1] < t[1]:
                return True
            # (b) j = y and i > x
            elif s[1] == t[1] and s[0] > t[0]:
                return True
            else:
                return False
        # Condition 2 (Both backward edges)
        elif s[0] > s[1] and t[0] > t[1]:
            # (a) i < x
            if s[0] < t[0]:
                return True
            # (b) i = x and j < y
            elif s[0] == t[0] and s[1] < t[1]:
                return True
            else:
                return False
        # Condition 3 (e_ij is forward edge and e_xy is backward edge)
        elif s[0] < s[1] and t[0] > t[1]:
            # j <= x
            if s[1] <= t[0]:
                return True
            else:
                return False
        # Condition 4 (e_ij is backward edge and e_xy is forward edge)
        elif s[0] > s[1] and t[0] < t[1]:
            # i < y
            if s[0] < t[1]:
                return True
            else:
                return False


def is_canonical(C):
    """ Checks if code C is canonical """

    Gc = build_graph(C)
    Dc = [Gc]  # graph corresponding to code C
    C_star = []
    for t in C:
        E = right_most_path_extensions(C_star, Dc)
        s, sup = find_min_edge(E)
        if is_smaller(s, t):
            return False
        C_star.append(s)
    return True


def gSpan(C, D, minsup):
    """
    Recursively mines a database of graphs to determine all frequent subgraphs.

    Keyword arguments:
    C -- a canonical and frequent code (list of tuples)
    D -- a database of n graphs (list of graphs)
    minsup -- minimum support threshold (integer)
    """

    global num_call

    print "pattern {}".format(num_call)
    num_call += 1
    if not C:
        print "()"
    for t in C:
        print t
    print ""

    E = right_most_path_extensions(C, D)
    for (t, sup) in E:
        C_prime = C + [t]
        sup_C_prime = sup
        if sup_C_prime >= minsup and is_canonical(C_prime):
            gSpan(C_prime, D, minsup)


if __name__ == "__main__":
    # D = graph_reader.graph_reader("exampleG.txt")
    D = graph_reader.graph_reader("Compound_422.txt")
    gSpan([], D, 2)

    # # Test right_most_path without support count
    # E = right_most_path_extensions(None, D)
    # for g in E.values():
    # print g

    # # Test right_most_path with support count
    # E = right_most_path_extensions([], D)
    # for t, sup in E:
    # print "t: {}, sup: {}".format(t, sup)
    # print "Smallest t: {}".format(min(E))

    # # Test sub_graph forward edge
    # C = [(0, 1, 'a', 'a', '_'), (1, 2, 'a', 'b', '_')]
    # sub_graph_isomorphisms(C, D[0])

    # # Test sub_graph backward edge
    # C = [(0, 1, 'a', 'a', '_'), (1, 2, 'a', 'b', '_'), (2, 0, 'b', 'a', '_')]
    # sub_graph_isomorphisms(C, D[0])

    # # Test right_most_path
    # C = [(0, 1, 'a', 'a', '_'), (1, 2, 'a', 'b', '_'), (2, 0, 'b', 'a', '_')]
    # E = right_most_path_extensions(C, D)
    # print E
    # for t, sup in E:
    #     print "t: {}, sup: {}".format(t, sup)

    # # Test find_min_edge
    # E = [((1, 2, 'a', 'b', '_'), 1), ((0, 2, 'a', 'b', '_'), 1)] # test 2 forward
    # E = [((8, 5, 'a', 'b', '_'), 1), ((8, 1, 'a', 'b', '_'), 1)] # test 2 backward
    # E = [((7, 9, 'a', 'b', '_'), 1), ((8, 5, 'a', 'b', '_'), 1)] # test forward, backward
    # E = [((8, 5, 'a', 'b', '_'), 1), ((7, 9, 'a', 'b', '_'), 1)] # test backward, forward
    # E = [((0, 1, 'a', 'b', '_'), 1), ((0, 1, 'a', 'a', '_'), 1)] # test labels 1
    # E = [((0, 1, 'b', 'a', '_'), 1), ((0, 1, 'a', 'b', '_'), 1)] # test labels 2
    # E = [((0, 1, 'b', 'a', '_'), 1), ((0, 1, 'a', 'c', '_'), 1)] # test labels 3
    # print find_min_edge(E)

    # # Test is_canonical
    # C = [(0, 1, 'a', 'a', '_'), (0, 2, 'a', 'b', '_')]
    # print is_canonical(C)

    # # Test is_canonical 2
    # C = [(0, 1, 'a', 'a', '_'), (1, 2, 'a', 'b', '_'), (2, 0, 'b', 'a', '_')]
    # print is_canonical(C)

    # # Test is_canonical 3
    # C = [(0, 1, 'a', 'a', '_'), (1, 2, 'a', 'b', '_'), (2, 0, 'b', 'a', '_'), (0, 3, 'a', 'b', '_')]
    # print is_canonical(C)