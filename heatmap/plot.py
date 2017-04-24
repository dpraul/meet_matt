import time
import sys
import os
import json

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from heatmap import CONFIG

rows = CONFIG.get('rows')
cols = CONFIG.get('columns')
counter = 0


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

    # variables used if saving
    running = True
    all_data = {'live': []}

    def generate_data():
        while True:
            data = get_data()
            yield data

    def generate_and_record_data():
        while running:
            data = get_data()
            all_data['live'].append({
                'i': len(all_data['live']),
                't': time.time(),
                'd': data.tolist()
            })
            yield data

    def on_key_release(event):
        if event.key == 'enter':
            global counter
            print('Created new section: %s' % counter)
            all_data[str(counter)], all_data['live'] = all_data['live'], []
            counter += 1

    def update(data):
        im.set_array(data)
        return [im]

    if len(sys.argv) > 2:
        filename = '%s_%s.json' % (sys.argv[2], int(time.time()))
    else:
        filename = None

    if filename is None:
        # display fullscreen
        wm = plt.get_current_fig_manager()
        wm.window.state('zoomed')

        ani = animation.FuncAnimation(fig, update, generate_data, interval=0, blit=True)
        plt.show(block=True)
    else:
        print('Press Ctrl+C to save data as %s' % filename)
        ani = animation.FuncAnimation(fig, update, generate_and_record_data, interval=0, blit=True)
        fig.canvas.mpl_connect('key_release_event', on_key_release)
        try:
            plt.show(block=True)
        except (KeyboardInterrupt, AttributeError):
            print('Created new section: %s' % counter)
            all_data[str(counter)] = all_data.pop('live')
            if not os.path.exists('data'):
                os.makedirs('data')
            with open('data/%s' % filename, 'w') as f:
                json.dump(all_data, f)
