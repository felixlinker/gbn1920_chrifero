import json
from multivitamin.utils.parser import parse_graph

def pytest_addoption(parser):
    parser.addoption("--cfg", required=True)


def pytest_generate_tests(metafunc):
    cfg = None
    with open(metafunc.config.getoption('cfg')) as fp:
        cfg = json.load(fp)
    for graph_cfg in cfg['graphs']:
        graph_cfg['mv_graph'] = parse_graph(graph_cfg['mv_graph'])

    metafunc.parametrize('graph', cfg['graphs'])
