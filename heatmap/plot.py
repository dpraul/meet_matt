import time
import json

import matplotlib.pyplot as plt
import numpy as np

from serial import Serial

# Configuration
COM_PORT = 'COM4'
BAUD_RATE = 115200
MUX_DELAY = 10  # ms

ROWS = 3
COLS = 3


def main():
    # create the figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.imshow(np.zeros((ROWS, COLS), dtype=np.int), cmap='hot', interpolation='nearest')
    plt.show(block=False)

    ser = Serial(COM_PORT, BAUD_RATE)
    # draw some data in loop
    while True:
        line = ser.readline()
        data = json.loads(line)
        print(data)
        if 'error' in data:
            print('Error: %s' % data['error'])
        else:
            # replace the image contents
            im.set_array(np.asarray(data['data'], dtype=np.int))
            # redraw the figure
            fig.canvas.draw()

if __name__ == '__main__':
    main()
