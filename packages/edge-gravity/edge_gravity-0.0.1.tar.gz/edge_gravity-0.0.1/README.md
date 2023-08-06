# edge_gravity

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