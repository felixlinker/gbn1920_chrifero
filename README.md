
# trier

This repository provides a library that does four things:

1. Read a set of graphs
2. Calculate the distances between the graphs
3. Calculate a phylogentic tree from this distance
4. Use the phylogentic tree as guide-tree for alignment, i.e. align graphs that are children of the same parent in the tree from leafs to root

## Prequisites

This library builds ontop of [MIGRAINE (forked)](https://github.com/felixlinker/MIGRAINE) and [multivitamin](https://github.com/mk36fyvy/multivitamin/).
The former is only used for benchmarking in `/benchmarks`, the latter is used by the library itself.

If you don't want to perform benchmarks, you can strip MIGRAINE from the Pipfile.

To be able to use this repository, first run `pipenv install`.
The two repositories listed above must be cloned in the parent folder, e.g.:
```
+-  gbn1920_chrifero/
    |
    +- README.md (you are here)
+-  multivitamin/
+-  MIGRAINE/
```

Obiously, you need to have [`pipenv`](https://github.com/pypa/pipenv) installed.

## Usage

Command line options are documented.
To execute the library via CLI, execute:
```
pipenv run python -m trier -h
```
