from time import sleep

import numpy as np
import matplotlib.pyplot as plt

from heatmap import CONFIG

rows = CONFIG.get('rows')
cols = CONFIG.get('columns')


def initial_heatmap_data():
    """

    :return: An array with data spanning all possible values, min to max, of heatmap
    """
    a = np.ones((rows, cols), dtype=np.int) * CONFIG.get('min')
    a[0][0] = CONFIG.get('max')
    return a


def main(get_data, wait=100):
    """

    :param get_data: A function that, when ran, samples data for the heatmap
    :param int wait: ms to sleep between calls
    :return:
    """
    # create the figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # must initialize with an array spanning all possible values
    im = ax.imshow(initial_heatmap_data(), cmap='hot', interpolation='nearest')
    # add colorbar to make data more readable
    plt.colorbar(im, orientation='horizontal')
    plt.show(block=False)  # block=False allows this to exist in a loop

    while True:
        data = get_data()
        im.set_array(data)
        fig.canvas.draw()
        sleep(wait / 1000.0)
