from migraine.VF2_pair_multi_flash import VF2_GraphAligner
from migraine.GraphIO import GraphIO
from os.path import split
from functools import reduce

graphs = []

def f_to_params(file):
    name = split(file)[-1].split(".")[0]
    graph = GraphIO.parse_file(file, name)
    return graph

def setup(inputs):
    global graphs
    graphs = list(map(f_to_params, inputs))

def aggregator(aggr, v):
    aligner = VF2_GraphAligner([aggr, v])
    return aligner.vf2_pga()

def run():
    global graphs
    reduce(aggregator, graphs)
