from argparse import ArgumentParser
from glob import glob
from itertools import chain
from multivitamin.utils.parser import parse_graph

from trier.scoring import Symmetric

scorers = dict(map(lambda c: (c.__name__, c), [Symmetric]))

parser = ArgumentParser()
parser.add_argument('--inputs', '-i', type=str, nargs='+', required=True)
parser.add_argument('--scorer', '-s', choices=scorers.keys(),
                    default=Symmetric.__name__)
args = parser.parse_args()

inputs = chain.from_iterable(map(glob, args.inputs))
graphs = map(parse_graph, inputs)
scorer = scorers[args.scorer](list(graphs))

print(scorer)
