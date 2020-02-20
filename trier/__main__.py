from argparse import ArgumentParser
from glob import glob
from multivitamin.utils.parser import parse_graph
from multivitamin.utils.graph_writer import write_graph
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor
import Bio.Phylo as Phylo
from os import path
from pathlib import Path

from trier.scoring import Symmetric, ComponentScorer, CroppingScorer
from trier.scoring.util import score_to_distance
from trier.aligning import GuidedAligning
from trier.util.func import concat

scorers = dict(map(lambda c: (c.__name__, c), [
               Symmetric, ComponentScorer, CroppingScorer]))

parser = ArgumentParser(
    description="""trier is a library that comes with a command line interface.
    You are executing the CLI right now.
    In a nutshell, this CLI executes the following steps:
    Read a list of graphs,
    calculate the distance between the graphs,
    construct a guide-tree for alignment,
    calculate the alignment.
    """)
parser.add_argument('--inputs', '-i', type=str, nargs='+', required=True,
                    help="""List of paths to .graph files. File names may
                    contain wildcards, e.g. ./my-path/*.graph""")
parser.add_argument('--scorer', '-s', choices=scorers.keys(),
                    default=Symmetric.__name__,
                    help="""Name of the scorer to calculate the scoring. """)
parser.add_argument('--outdir', '-o', type=str, required=False,
                    help="""Directory to write results to; if none is given,
                    nothing will be written.""")
parser.add_argument('--no-alignment', '-A', action='store_true',
                    help="""If this flag is set, only the distance-matrix and
                    the guide-tree will be calculated; the guide-tree will not
                    be traversed.""")
parser.add_argument('--tree', '-t', type=str, required=False, default=None,
                    help="""Path to phylogenetic tree file. Leafs of the tree
                    must be labelled with the corresponding graph files names
                    without file extension. If this argument is given, the
                    guide-tree calculation will be skipped and this tree is
                    used instead.""")
args = parser.parse_args()

inputs = concat(map(glob, args.inputs))
graphs = list(map(parse_graph, inputs))

tree = None
if args.tree is None:
    scorer = scorers[args.scorer](graphs)
    scorer.calc_scoring()
    distance = score_to_distance(scorer.get_scoring())
    tree_constructor = DistanceTreeConstructor()
    tree = tree_constructor.upgma(distance)

    if args.outdir:
        Path(args.outdir).mkdir(parents=True, exist_ok=True)
        with open(path.join(args.outdir, 'distance.phylip'), 'w') as handle:
            distance.format_phylip(handle)
        Phylo.write(tree, path.join(args.outdir, 'guide.newick'), 'newick')
else:
    tree = next(Phylo.parse(args.tree, args.tree.split('.')[-1]))

if not args.no_alignment:
    aligner = GuidedAligning(graphs, tree)
    aligning = aligner.calc_aligning()
    if args.outdir:
        for k, g in aligning.items():
            write_graph(g, args.outdir, k + '.graph')
