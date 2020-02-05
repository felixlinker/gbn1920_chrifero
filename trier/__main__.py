from argparse import ArgumentParser
from glob import glob
from itertools import chain
from multivitamin.utils.parser import parse_graph

from .scoring import Symmetric

scorers = {
    'symmetric': Symmetric,
}

parser = ArgumentParser()
parser.add_argument('--inputs', '-i', type=list, nargs='+')
parser.add_argument('--scorer', '-s', choices=scorers.keys())
args = parser.parse_args()

inputs = chain.from_iterable(map(glob, args.inputs))
graphs = map(parse_graph, inputs)
scorer = scorers[args.scorer](list(graphs))

print(scorer)
