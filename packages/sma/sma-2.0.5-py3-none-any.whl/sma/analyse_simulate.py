#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sma
import itertools
import networkx as nx
import multiprocessing

class _simulateBaselineAutoMapper:
    def __init__(self, motifs, assume_sparse):
        self.motifs = motifs
        self.assume_sparse = assume_sparse
    def __call__(self, G):
        partial, _ = sma.countMotifsAuto(G, *self.motifs, assume_sparse = self.assume_sparse)
        return partial

def simulateBaselineAuto(G : nx.Graph, 
                         *motifs, 
                         n = 100,
                         processes = 0,
                         chunksize = 100,
                         assume_sparse = False,
                         model = sma.MODEL_ERDOS_RENYI):
    """
    Simulates a random baseline of graphs similar to a given SEN and counts motifs
    in these randomly generated graphs.
    
    :param G: the SEN
    :param motifs: motif identifier strings of motifs that shall be counted
    :param n: number of iterations
    :param processes: number of processes, default zero (no multiprocessing)
    :param chunksize: chunksize for multiprocessing
    :param assume_sparse: whether the random graphs shall be assumed to be sparse.
        Used to find an ideal counter, cf. :py:meth:`sma.findIdealCounter`.
    :param model: model to be used, currently only :py:const:`sma.MODEL_ERDOS_RENYI`
        is implemented
    :returns: dict mapping motif identifiers to list of counts
    """
    if model == sma.MODEL_ERDOS_RENYI:
        random_networks = sma.randomSimilarMultiSENs(G)
    else:
        raise NotImplementedError("model %s not implemented" % model)
    source = itertools.islice(random_networks, n)
    mapper = _simulateBaselineAutoMapper(motifs, assume_sparse)
    result = {k : [] for k in motifs}
    if processes <= 0:
        for row in map(mapper, source):
            for k, v in row.items():
                result[k].append(v)
            del row
    else:
        with multiprocessing.Pool(processes) as p:
            rows = p.imap_unordered(mapper, source, chunksize = chunksize)
            for row in rows:
                for k, v in row.items():
                    result[k].append(v)
                del row
            p.close()
            p.join()        
    return result
                
            
    