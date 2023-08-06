from collections import defaultdict, Counter
from concurrent.futures import ProcessPoolExecutor
from itertools import islice
import math
from multiprocessing import cpu_count
import random

import networkx as nx

cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
cdef is_subsequence(tuple subseq, tuple seq):
    """used to check if an edge is present in a path"""
    cdef int len_subseq, len_seq, start, end
    len_subseq = 2
    len_seq = len(seq)
    start = 0
    end = len_subseq
    for _ in range(len_seq - len_subseq + 1):
        if seq[start:end] == subseq:
            return True
        start += 1
        end = start + len_subseq
    else:
        return False

def chunks(iterable, chunksize):
        iterable = iter(iterable)
        temp = [next(iterable)]

        for item in iterable:
            if not len(temp) % chunksize:
                yield temp
                temp = []
            temp.append(item)

        yield temp

def worker(args):
    """
    does the heavy lifting - every process gets a worker and every worker a subset of#
    nodes for which the calculations are done. The results are added up at the end.
    """
    cdef list nodelist
    cdef int k
    cdef str u, v
    cdef tuple edge, edges, tuple_path

    g, nodelist, k, weight = args
    l = defaultdict(int)

    def get_shortest_paths(g, list nodelist, int k, weight):

        cdef tuple nodes = tuple(g.nodes())
        cdef str u, v

        for u in nodelist:
            for v in nodes:
                if u != v:
                    try:
                        for path in islice(nx.shortest_simple_paths(g, u, v, weight=weight), k):
                            yield (u, v, path)
                    except nx.NetworkXNoPath:
                        pass

    k_counter = defaultdict(int)
    edges = tuple(g.edges())

    for u, v, shortest_paths in get_shortest_paths(g, nodelist, k, weight):
        tuple_path = tuple(shortest_paths)
        k_counter[tuple([u,v])] += 1
        for edge in edges:
            if is_subsequence(edge, tuple_path):
                l[tuple(edge)] += 1

    return k_counter, l

def edge_gravity(g, k=None, weight=None):
    """
    Function that calculates Edge Gravity as described in:
        Helander, M.E. & McAllister, S. Appl Netw Sci (2018) 3: 7.
        https://doi.org/10.1007/s41109-018-0063-6

    The k-shortest-paths algorithm stems from:
        Jin Y. Yen, "Finding the K Shortest Loopless Paths in a
       Network", Management Science, Vol. 17, No. 11, Theory Series
       (Jul., 1971), pp. 712-716

    It utilizes multiple cores, only tested on Linux.

    Parameters
    ----------
    g: NetworkX DiGraph

    k: non-negative Integer that describes the maximum number of shortest
        path to consider per node.

    weight: gets passed to networkx.shortest_simple_paths - for a detailed description
        see the docstring of this function.

    Returns
    ----------
    A 2-tuple where 
        the first element is either kstar or False if kstar is not known
        the second element is a collections.Counter object with edges as keys and the number of paths as values
    """

    if k == None:
        k = 999_999

    with ProcessPoolExecutor(max_workers=cpu_count()) as exe:

        futures = []
        nodes = list(g.nodes())
        random.shuffle(nodes)

        for chunk in chunks(nodes, math.ceil(len(g.nodes()) / cpu_count() * .3)):
            futures.append(exe.submit(worker, (g, chunk, k, weight)))

        results = [future.result() for future in futures]
        k_counters, gravity_counters = list(zip(*results))

        k_result = Counter()
        for r in k_counters:
            k_result += r

        gravity_result = Counter()
        for r in gravity_counters:
            gravity_result += r

        if max(k_result.values()) >= k:
            kstar = False
        else:
            kstar = max(k_result.values())

    return kstar, gravity_result
