import argparse
import timeit

libraries= {
    'multivitamin': {
        'stmt': 'from bm_multivitamin import run; run()',
        'setup': 'from bm_multivitamin import setup; setup(args.inputs)',
    },
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputs', '-i', nargs='+')
    parser.add_argument('--library', '-l', choices=libraries.keys())
    parser.add_argument('--number', '-n', type=int, default=20)
    args = parser.parse_args()

    duration = timeit.timeit(globals=globals(), **
                             libraries[args.library], number=args.number)
    print(duration)
