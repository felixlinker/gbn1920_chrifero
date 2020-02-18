from argparse import ArgumentParser
from glob import glob
from multivitamin.utils.parser import parse_graph
from multivitamin.utils.graph_writer import write_graph
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor
import Bio.Phylo as Phylo
from os import path
from pathlib import Path

from trier.scoring import Symmetric, ComponentScorer, CroppingScorer
from trier.aligning import GuidedAligning
from trier.util.func import concat

scorers = dict(map(lambda c: (c.__name__, c), [Symmetric, ComponentScorer, CroppingScorer]))

parser = ArgumentParser()
parser.add_argument('--inputs', '-i', type=str, nargs='+', required=True)
parser.add_argument('--scorer', '-s', choices=scorers.keys(),
                    default=Symmetric.__name__)
parser.add_argument('--outdir', '-o', type=str, required=False)
args = parser.parse_args()

inputs = concat(map(glob, args.inputs))
graphs = list(map(parse_graph, inputs))
scorer = scorers[args.scorer](graphs)
scorer.calc_scoring()
tree_constructor = DistanceTreeConstructor()
tree = tree_constructor.upgma(scorer.get_scoring())
aligner = GuidedAligning(graphs, tree)
aligning = aligner.calc_aligning()
print(aligning)

if args.outdir:
    Path(args.outdir).mkdir(parents=True, exist_ok=True)
    with open(path.join(args.outdir, 'scoring.phylip'), 'w') as handle:
        scorer.get_scoring().format_phylip(handle)
    Phylo.write(tree, path.join(args.outdir, 'guide.newick'), 'newick')
    for k, g in aligning.items():
        write_graph(g, args.outdir, k)
