#!/usr/bin/env python

import copy
import graph
import graph_reader


__author__ = 'Jamie Fujimoto'


def build_graph(C):
    g = graph.Graph(1)
    for t in C:
        g.add_ext(t)
    return g


def sub_graph_isomorphisms(C, G):
    """

    :param C:
    :param G:
    :return:
    """
    # print "C: {}".format(C)
    # phi = {i: [x] for i, x in enumerate(G.get_vertex_by_label(C[0][2]))}
    phi = [[x] for x in G.get_vertex_by_label(C[0][2])]  # changed from dict to list
    # print "phi: {}".format(phi)
    for t in C:
        u, v, u_label, v_label, edge_label = t
        # phi_prime = {}  # changed from dict to list
        phi_prime = []
        # for p in phi.values():  # changed from dict to list
        for p in phi:
            # print "p: {}".format(p)
            # print "u: {}".format(u)
            # print "p[u]: {}".format(p[u])
            if v > u:
                # forward edge
                for x in G.get_neighbors(p[u]):
                    if (x not in p) and \
                       (G.get_vertex_label(x) == v_label) and \
                       (G.get_edge_label(p[u], x) == edge_label):
                        # print "x: {}".format(x)
                        p_prime = p + [x]
                        # print "p_prime: {}".format(p_prime)
                        phi_prime.append(p_prime)
                        # print "phi_prime: {}".format(phi_prime)
            else:
                # backward edge
                # print "p[v]: {}".format(p[v])
                if p[v] in G.get_neighbors(p[u]):
                    phi_prime.append(p)
                    # print "phi_prime: {}".format(phi_prime)
        phi = copy.copy(phi_prime)
        # print "updated phi: {}".format(phi)
    return copy.copy(phi)


def right_most_path_extensions(C, D):
    """

    :param C: a canonical and frequent code
    :param D: a database of n graphs
    :return: set of edge extensions along with their support values
    """

    Gc = build_graph(C)
    # print "C: {}".format(C)
    R = [v.id for v in Gc]  # nodes on the rightmost path in C
    # print "R: {}".format(R)
    if R:
        u_r = R[-1]  # rightmost child in C (DFS number)
    else:
        u_r = None
    # print "u_r: {}".format(u_r)
    E = {}  # set of extensions from C

    for G in D:
        E[G.id] = []
        if not C:
            # add distinct label tuples in Gi as forward extensions
            # E[G.id] = []
            # distinct = 0
            for dist_tuple in G.get_distinct_label_tuples():
                E[G.id].append((0, 1) + dist_tuple)
                # E[G.id][distinct] = (0, 1) + dist_tuple
                # distinct += 1
        else:
            # print "C: {}".format(C[0][2])
            phi = sub_graph_isomorphisms(C, G)
            for p in phi:  # for each isomorphism in phi
                # print "C: {}".format(C)
                # print "p: {}".format(p)
                # print "u_r: {}".format(u_r)

                # backward extensions from rightmost child
                # print "neighbors: {}".format(G.get_neighbors(p[u_r]))
                for x in G.get_neighbors(p[u_r]):
                    # print "x = {} label: {}".format(x, G.get_vertex_label(x))
                    vs = Gc.get_vertex_by_label(G.get_vertex_label(x))
                    # print "vs = {}".format(Gc.get_vertex_by_label(G.get_vertex_label(x)))
                    valid_v = [v for v in vs if (p[v] == x) and (v in R) and ((u_r, v) not in Gc.connections)]
                    # print "valid_v: {}".format(valid_v)
                    for v in valid_v:
                        # print G.connections
                        b = (u_r, v, Gc.get_vertex_label(u_r), Gc.get_vertex_label(v), G.get_edge_label(p[u_r], p[v]))
                        E[G.id].append(b)

                # forward extension from nodes on rightmost path
                for u in R:
                    print "u: {} label: {}".format(u, Gc.get_vertex_label(u))
                    neigbors = [n for n in G.get_neighbors(p[u]) if n not in p]
                    print "neighbors: {}".format(neigbors)
                    for x in neigbors:
                        print "x: {} label: {}".format(x, G.get_vertex_label(x))
                        E[G.id].append((u, u_r + 1, Gc.get_vertex_label(u), G.get_vertex_label(x), G.get_edge_label(p[u], x)))

            # print "E: {}".format(E)
    # compute the support of each extension
    sup = {}
    for G in E.values():
        for ext in G:
            if ext not in sup:
                sup[ext] = 1
            else:
                sup[ext] += 1
    # return E
    return sorted(sup.items())


def is_canonical(C):
    """

    :param C:
    :return:
    """
    Dc = [build_graph(C)]  # graph corresponding to code C
    C_star = []
    for t in C:
        E = right_most_path_extensions(C_star, Dc)
        # print "E in is_canonical: {}".format(E)
        (s, sup) = min(E)
        # print "(s, sup): {}".format((s,sup))
        if s < t:
            # print "returning False"
            return False
        C_star = C_star + [s]
    return True


def gSpan(C, D, minsup):
    """
    First determines the set of possible edge extensions along the rightmost path.

    :param C: a canonical and frequent code
    :param D: a database of n graphs
    :param minsup: minimum support threshold
    :return:
    """
    E = right_most_path_extensions(C, D)
    for (t, sup) in E:
        C_prime = C + [t]
        sup_C_prime = sup
        if sup_C_prime >= minsup and is_canonical(C_prime):
            gSpan(C_prime, D, minsup)


if __name__ == "__main__":
    D = graph_reader.graph_reader("exampleG.txt")

    # # Test right_most_path without support count
    # E = right_most_path_extensions(None, D)
    # for g in E.values():
    # print g

    # # Test right_most_path with support count
    # E = right_most_path_extensions([], D)
    # for t, sup in E:
    # print "t: {}, sup: {}".format(t, sup)
    # print "Smallest t: {}".format(min(E))

    # gSpan([], D, 2)

    # # Test sub_graph forward edge
    # C = [(0, 1, 'a', 'a', '_'), (1, 2, 'a', 'b', '_')]
    # sub_graph_isomorphisms(C, D[0])

    # # Test sub_graph backward edge
    # C = [(0, 1, 'a', 'a', '_'), (1, 2, 'a', 'b', '_'), (2, 0, 'b', 'a', '_')]
    # sub_graph_isomorphisms(C, D[0])

    # # Test right_most_path
    # E = right_most_path_extensions([(0, 1, 'a', 'a', '_'), (1, 2, 'a', 'b', '_')], D)
    # for t, sup in E:
    #     print "t: {}, sup: {}".format(t, sup)
    # print "Smallest t: {}".format(min(E))