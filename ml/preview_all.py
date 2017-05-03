import os
import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from heatmap import CONFIG

from ml.extract_data import get_samples

rows = CONFIG.get('rows')
cols = CONFIG.get('columns')
IMAGE_PATH = 'tmp/img'

if not os.path.exists(IMAGE_PATH):
    os.mkdir(IMAGE_PATH)


def initial_heatmap_data():
    """

    :return: An array with data spanning all possible values, min to max, of heatmap
    """
    a = np.ones((rows, cols), dtype=np.int) * CONFIG.get('min')
    a[0][0] = CONFIG.get('max')
    return a


def main():
    # create the figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # must initialize with an array spanning all possible values
    im = ax.imshow(initial_heatmap_data(), cmap='hot', interpolation='nearest')
    # add colorbar to make data more readable
    plt.colorbar(im, orientation='horizontal')

    all_data, filenames = get_samples()

    def get_data():
        for label, samples in all_data.items():
            for i, sample in enumerate(samples):
                yield sample
                path = os.path.join(IMAGE_PATH, label)
                if not os.path.exists(path):
                    os.mkdir(path)
                fig.savefig('%s/%s.png' % (path, filenames[label][i]))
        sys.exit(0)

    def update(data):
        im.set_array(data)
        return [im]

    # display fullscreen
    #wm = plt.get_current_fig_manager()
    #wm.window.state('zoomed')

    ani = animation.FuncAnimation(fig, update, get_data, interval=0, blit=True)
    plt.show(block=True)
