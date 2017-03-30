import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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


def main(get_data):
    """

    :param get_data: A function that, when ran, samples data for the heatmap
    :return:
    """
    # create the figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # must initialize with an array spanning all possible values
    im = ax.imshow(initial_heatmap_data(), cmap='hot', interpolation='nearest')
    # add colorbar to make data more readable
    plt.colorbar(im, orientation='horizontal')
    # display fullscreen
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')

    def data_gen():
        while True:
            data = get_data()
            yield data

    def update(data):
        im.set_array(data)
        return [im]

    ani = animation.FuncAnimation(fig, update, data_gen, interval=0, blit=True)

    plt.show(block=True)