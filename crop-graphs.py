from trier.graph.adjacency import AdjacencyGraph
from trier.graph.crop import crop_graph
from trier.util.func import concat
from argparse import ArgumentParser
from multivitamin.utils.parser import parse_graph
from multivitamin.utils.graph_writer import write_graph
from glob import glob
from pathlib import Path

parser = ArgumentParser()
parser.add_argument('--inputs', '-i', type=str, nargs='+', required=True)
parser.add_argument('--outdir', '-o', type=str, required=False)
args = parser.parse_args()

graphs = map(parse_graph, concat(map(glob, args.inputs)))
for g in graphs:
    adj = AdjacencyGraph(graph=g)
    cropped = crop_graph(adj)
    Path(args.outdir).mkdir(parents=True, exist_ok=True)
    write_graph(cropped.to_multivitamin(), args.outdir, f'{cropped.id}.graph')
