import numpy as np

from heatmap import CONFIG

rows = CONFIG.get('rows')
cols = CONFIG.get('columns')


def get_data():
    while True:
        yield np.random.randint(0, 1024, size=(rows, cols))
