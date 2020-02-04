import argparse
import timeit
from glob import glob
from itertools import chain

libraries = {
    'multivitamin': {
        'stmt': 'from bm_multivitamin import run; run()',
        'setup': 'from bm_multivitamin import setup; setup(inputs[:slice_to])',
    },
}

parser = argparse.ArgumentParser()
parser.add_argument('--inputs', '-i', nargs='+')
parser.add_argument('--library', '-l', choices=libraries.keys())
parser.add_argument('--number', '-n', type=int, default=5)
parser.add_argument('--asc', '-a', action='store_true')
args = parser.parse_args()

def run(i):
    global slice_to
    slice_to = i + 1
    return timeit.timeit(globals=globals(), number=args.number,
                         **libraries[args.library])

inputs = list(chain.from_iterable(map(glob, args.inputs)))
durations = map(
    run,
    range(1 if args.asc else len(inputs) - 1, len(inputs))
)
print(list(durations))
