import sys
import os
import json

import numpy as np

from heatmap import CONFIG

rows = CONFIG.get('rows')
cols = CONFIG.get('columns')


def print_debug(r):
    print('sections: %s' % len(r))
    for section in range(len(r)):
        s = str(section)
        print('r[%s]: len(%s)' % (s, len(r[s])))


def get_data():
    if len(sys.argv) < 3:
        raise ValueError('You must enter a file to replay')
    filename = sys.argv[2]
    if not os.path.isfile(filename):
        raise IOError('Input file %s does not exist' % filename)

    with open(filename) as f:
        r = json.load(f)

    print_debug(r)

    if len(sys.argv) == 5:  # request a single frame
        section = str(sys.argv[3])
        i = int(sys.argv[4])
        while True:
            yield np.asarray(r[section][i]['d'])
    else:
        section = 0
        i = 0
        while True:
            yield np.asarray(r[str(section)][i]['d'])
            i += 1
            if i >= len(r[str(section)]):
                section += 1
                i = 0
            if section >= len(r):
                section = 0
