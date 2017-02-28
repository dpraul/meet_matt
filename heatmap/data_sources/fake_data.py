import numpy as np

from heatmap import CONFIG

rows = CONFIG.get('rows')
cols = CONFIG.get('columns')


def get_data():
    return np.random.randint(0, 600, size=(rows, cols))
