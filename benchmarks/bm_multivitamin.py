from multivitamin.utils.multalign import Multalign
from multivitamin.utils.parser import parse_graph

aligner = None

def setup(inputs):
    global aligner
    aligner = Multalign(
        # input_files is a magical global constant set by benchmark.py
        graph_list=list(map(parse_graph, inputs)),
        algorithm='SUBVF2',
        method='GREEDY',
        save_all=False
    )

def run():
    global aligner
    return aligner.multalign()
