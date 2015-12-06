#!/usr/bin/env python


import graph_reader
import gspan
import sys


__author__ = 'Jamie Fujimoto'


def script():
    filename = sys.argv[1]
    min_sup = sys.argv[2]

    D = graph_reader.graph_reader(filename)
    gspan.gSpan([], D, int(min_sup))

    print "Total number of patterns: {}".format(gspan.num_call - 1)


if __name__ == "__main__":
    script()