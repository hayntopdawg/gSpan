#!/usr/bin/env python
import graph
import graph_reader


__author__ = 'Jamie Fujimoto'


def sub_graph_isomorphism(C, Gi):
    """

    :param C:
    :param Gi:
    :return:
    """
    pass


def right_most_path_extensions(C, D):
    """

    :param C: a canonical and frequent code
    :param D: a database of n graphs
    :return: set of edge extensions along with their support values
    """

    R = None  # nodes on the rightmost path in C
    u_r = None  # rightmost child in C (DFS number)
    E = {}  # set of extensions from C

    for g in D:
        if not C:
            # add distinct label tuples in Gi as forward extensions
            E[g.id] = []
            # distinct = 0
            for dist_tuple in g.get_distinct_label_tuples():
                E[g.id].append((0, 1) + dist_tuple)
                # E[g.id][distinct] = (0, 1) + dist_tuple
                # distinct += 1
        else:
            # psi = sub_graph_isomorphism(C, G)
            pass
    # compute the support of each extension
    sup = {}
    for g in E.values():
        for ext in g:
            if ext not in sup:
                sup[ext] = 1
            else:
                sup[ext] += 1
    # return E
    return sorted(sup.items())


def build_graph(C):
    g = graph.Graph(1)
    for t in C:
        g.add_ext(t)
    return g


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
    # E = right_most_path_extensions(None, D)
    # for g in E.values():
    #     print g
    # E = right_most_path_extensions([], D)
    # for (t, sup) in E:
    #     print t
    #     print sup
    # print min(E)
    gSpan([], D, 2)