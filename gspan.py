#!/usr/bin/env python

import copy
import graph
import graph_reader


__author__ = 'Jamie Fujimoto'


num_call = 1


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

# why does right most path return empty lists?
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
                    # print "u: {} label: {}".format(u, Gc.get_vertex_label(u))
                    neigbors = [n for n in G.get_neighbors(p[u]) if n not in p]
                    # print "neighbors: {}".format(neigbors)
                    for x in neigbors:
                        # print "x: {} label: {}".format(x, G.get_vertex_label(x))
                        E[G.id].append((u, u_r + 1, Gc.get_vertex_label(u), G.get_vertex_label(x), G.get_edge_label(p[u], x)))

            # print "E: {}".format(E)
    # compute the support of each extension
    sup = {}
    # print "E: {}".format(E)
    for G in E:
        # make each list of tuples distinct
        distinct_exts = list(set(E[G]))
        # print "distinct_exts: {}".format(distinct_exts)
        for ext in distinct_exts:
            if ext not in sup:
                sup[ext] = 1
            else:
                sup[ext] += 1
    # return E
    # print "sup.items(): {}".format(sup.items())
    sorted_tuples = sort_tuples(sup.items())
    # print "sorted_tuples: {}".format(sorted_tuples)
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
        # # (i, j) = (x, y)
        # elif min_edge[0] == edge[0] and min_edge[1] == edge[1]:
        #     if edge < min_edge:
        #         min_edge, min_edge_sup = edge, sup
        else:
            # if edge is smaller than min_edge
            if is_smaller(edge, min_edge):
                min_edge, min_edge_sup = edge, sup
            # # Condition 1 (Both forward edges)
            # if min_edge[0] < min_edge[1] and edge[0] < edge[1]:
            #     # (a) j < y
            #     if edge[1] < min_edge[1]:
            #         min_edge, min_edge_sup = edge, sup
            #     # (b) j = y and i > x
            #     elif edge[1] == min_edge[1] and edge[0] > min_edge[0]:
            #         min_edge, min_edge_sup = edge, sup
            # # Condition 2 (Both backward edges)
            # elif min_edge[0] > min_edge[1] and edge[0] > edge[1]:
            #     # (a) i < x
            #     if edge[0] < min_edge[0]:
            #         min_edge, min_edge_sup = edge, sup
            #     # (b) i = x and j < y
            #     elif edge[0] == min_edge[0] and edge[1] < min_edge[1]:
            #         min_edge, min_edge_sup = edge, sup
            # # Condition 3 (e_ij is forward edge and e_xy is backward edge)
            # elif edge[0] < edge[1] and min_edge[0] > min_edge[1]:
            #     # j <= x
            #     if edge[1] <= min_edge[0]:
            #         min_edge, min_edge_sup = edge, sup
            # # Condition 4 (e_ij is backward edge and e_xy is forward edge)
            # elif edge[0] > edge[1] and min_edge[0] < min_edge[1]:
            #     # i < y
            #     if edge[0] < min_edge[1]:
            #         min_edge, min_edge_sup = edge, sup
    # print "E: {}".format(E)
    return min_edge, min_edge_sup


def is_smaller(s, t):
    # print "s: {} t: {}".format(s, t)
    if not s:
        return False  # Should this be True or False?  Or not needed if right most is fixed?
    # (i, j) = (x, y)
    elif s[0] == t[0] and s[1] == t[1]:
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
    """

    :param C:
    :return:
    """
    # print "C in is_canonical: {}".format(C)
    Dc = [build_graph(C)]  # graph corresponding to code C
    C_star = []
    for t in C:
        # print "t in is_canonical: {}".format(t)
        E = right_most_path_extensions(C_star, Dc)
        # print "E in is_canonical: {}".format(E)
        s, sup = find_min_edge(E)
        # print "(s, sup): {}".format((s,sup))
        if is_smaller(s, t):
            # print "{} is not canonical. {} is smaller".format(t, s)
            return False
        if s:  # removes empty list
            C_star.append(s)
        # print "C_star in is_canonical: {}".format(C_star)
    # print "{} is canonical".format(t)
    return True


def gSpan(C, D, minsup):
    """
    First determines the set of possible edge extensions along the rightmost path.

    :param C: a canonical and frequent code
    :param D: a database of n graphs
    :param minsup: minimum support threshold
    :return:
    """
    global num_call

    print "pattern {}".format(num_call)
    num_call += 1
    print C

    E = right_most_path_extensions(C, D)
    # print "E: {}".format(E)
    for (t, sup) in E:
        C_prime = C + [t]
        sup_C_prime = sup
        if sup_C_prime >= minsup and is_canonical(C_prime):
            gSpan(C_prime, D, minsup)


if __name__ == "__main__":
    D = graph_reader.graph_reader("exampleG.txt")
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

    # # Test is_canonical
    # C = [(0, 1, 'a', 'a', '_'), (1, 2, 'a', 'b', '_'), (2, 0, 'b', 'a', '_')]
    # print is_canonical(C)