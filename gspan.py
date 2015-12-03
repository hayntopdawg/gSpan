#!/usr/bin/env python
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


def is_canonical(C_prime):
    """

    :param C_prime:
    :return:
    """
    pass


def gSpan(C, D, minsup):
    """
    First determines the set of possible edge extensions along the rightmost path.

    :param C: a canonical and frequent code
    :param D: a database of n graphs
    :param minsup: minimum support threshold
    :return:
    """
    E = right_most_path_extensions(C, D)


if __name__ == "__main__":
    D = graph_reader.graph_reader("exampleG.txt")
    # E = right_most_path_extensions(None, D)
    # for g in E.values():
    #     print g
    sup = right_most_path_extensions(None, D)
    print sup