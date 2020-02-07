from argparse import ArgumentParser
from glob import glob
from itertools import chain
from multivitamin.utils.parser import parse_graph
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor

from trier.scoring import Symmetric
from trier.aligning import GuidedAligning

scorers = dict(map(lambda c: (c.__name__, c), [Symmetric]))

parser = ArgumentParser()
parser.add_argument('--inputs', '-i', type=str, nargs='+', required=True)
parser.add_argument('--scorer', '-s', choices=scorers.keys(),
                    default=Symmetric.__name__)
args = parser.parse_args()

inputs = chain.from_iterable(map(glob, args.inputs))
graphs = map(parse_graph, inputs)
scorer = scorers[args.scorer](list(graphs))
scorer.calc_scoring()
tree_constructor = DistanceTreeConstructor()
tree = tree_constructor.upgma(scorer.get_scoring())
aligner = GuidedAligning(graphs, tree)
aligning = aligner.calc_aligning()
print(aligning)
