import sys

from algorithms import compute_support, load_graphs
from algorithms import g_span

# Lookup table for elements
elem_lup = {1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C', 7: 'N', 8: 'O',
            9: 'F', 10: 'Ne', 11: 'Na', 12: 'Mg', 13: 'Al', 14: 'Si', 15: 'P',
            16: 'S', 17: 'Cl', 18: 'Ar', 19: 'K', 20: 'Ca', 21: 'Sc', 22: 'Ti',
            23: 'V', 24: 'Cr', 25: 'Mn', 26: 'Fe', 27: 'Co', 28: 'Ni', 29: 'Cu',
            30: 'Zn', 31: 'Ga', 32: 'Ge', 33: 'As', 34: 'Se', 35: 'Br',
            36: 'Kr',
            37: 'Rb', 38: 'Sr', 39: 'Y', 40: 'Zr', 41: 'Nb', 42: 'Mo', 43: 'Tc',
            44: 'Ru', 46: 'Pd', 47: 'Ag', 48: 'Cd', 49: 'In', 50: 'Sn',
            51: 'Sb',
            52: 'Te', 53: 'I', 54: 'Xe', 55: 'Cs', 56: 'Ba', 57: 'Hf', 58: 'Ta',
            59: 'W', 60: 'Re', 61: 'Os', 62: 'Ir', 64: 'Au', 65: 'Hg', 66: 'Tl',
            67: 'Pb', 68: 'Bi', 69: 'Po', 70: 'At', 71: 'Rn', 72: 'Fr',
            73: 'Ra',
            74: 'Pt', 75: 'Ac', 76: 'La', 77: 'U', 78: 'Sm', 79: 'Ce', 80: 'Nd',
            81: 'Eu', 82: 'Gd', 83: 'Dy', 84: 'Er', 85: 'Rh'}

# Lookup table for bonds
bond_lup = {1: '-', 2: '=', 3: '#'}


def get_toxicity(ground_truth_path='bbp2.groundTruth'):
    f = open(ground_truth_path, 'r')
    tox = [line.split(',')[2][0] for line in f.readlines()]
    f.close()
    return tox


def translate_pattern(idx, pat_supp, pat_def):
    """
    Translates the given pattern into the correct gspan' output format
    :param idx: pattern index
    :param pat_supp: pattern support
    :param pat_def: pattern definition
    :return: string
    """
    retString = '%s: %s\n' % (idx, pat_supp)
    for pat_def_line in pat_def:
        retString += '(%s, %s, %s, %s, %s)\n' % (
            pat_def_line[0], pat_def_line[1], elem_lup[int(pat_def_line[2])],
            bond_lup[int(pat_def_line[4])], elem_lup[int(pat_def_line[3])])
    retString += '\n'
    return retString


def translate_pattern_list(patterns):
    """
    Translates the pattern into the gspan' output format
    :param patterns: list of patterns
    :return: formatted string listing the patterns
    """
    outlines = ''
    patterns.sort()
    patterns.reverse()
    for i, (pat_supp, pattern) in enumerate(patterns):
        outlines += translate_pattern(i, pat_supp, pattern)
    return outlines


def graph_contains_pattern(graph, pattern):
    """
    Checks whether there exists a subgraph-isomorphism between the graph and
    the pattern
    :param graph: graph
    :param pattern: pattern
    :return: True if subgraph-isomorphism exists, else False
    """
    return True if compute_support(pattern, [graph, None]) else False


def load_dataset(f):
    """
    Loads a given dataset (.gsp file)
    :param f: dataset path
    :return: list of graphs
    """
    return load_graphs(f)


def run_gspan(train_path, test_path, min_sup, out_path='out.txt'):
    """
    Runs the gspan algorithm on the training set and tests the patterns
    against the test set for support
    :param train_path: Path to the training set
    :param test_path: Path to the test set
    :param min_sup: Minimum support threshold (absolute)
    :param out_path: Path to the output file
    :return: tuple: (train_database, test_database, patterns)
    """
    # Parse
    min_sup = int(min_sup)

    # Load the databases
    train_db = load_dataset(train_path)
    print('Number of training graphs: %s' % len(train_db))
    test_db = load_dataset(test_path)
    print('Number of testing graphs: %s' % len(test_db))

    print('Starting gSpan algorithm ...')
    train_pattern = []
    g_span([], train_db, min_sup=min_sup, extensions=train_pattern)

    # remove empty pattern
    train_pattern = list(
        map(list, filter(lambda x: x, set(map(tuple, train_pattern))))
    )
    print('Found %s pattern in the training set' % (len(train_pattern)))

    print('Generating output at %s' % out_path)
    pattern_supp_list = []
    for idx, pattern in enumerate(train_pattern):
        pat_supp = compute_support(pattern, test_db)
        pattern_supp_list.append((pat_supp, pattern))
    fh = open(out_path, 'w')
    fh.writelines(translate_pattern_list(pattern_supp_list))
    fh.close()
    return train_db, test_db, pattern_supp_list


if __name__ == '__main__':
    train_db, test_db, patterns = run_gspan(sys.argv[1], sys.argv[2],
                                            int(sys.argv[3]))

    print(patterns)
