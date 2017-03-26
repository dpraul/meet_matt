import struct

from serial import Serial
import numpy as np

from heatmap import CONFIG

COM_PORT = CONFIG.get('serial', {}).get('port', None)
BAUD_RATE = CONFIG.get('serial', {}).get('baud', None)

rows = CONFIG.get('rows')
cols = CONFIG.get('columns')

if COM_PORT is None or BAUD_RATE is None:
    raise KeyError('Baud rate and COM port must be specific in config to use serial communication.')

ser = Serial(COM_PORT, BAUD_RATE)


def get_data():
    data = np.empty([rows, cols], dtype=np.int16)
    # send start bit
    ser.write(bytearray([6]))
    # read each received int
    for i in range(rows):
        for j in range(cols):
            data[i, j] = struct.unpack('>H', ser.read(2))

    return np.asarray(data['data'], dtype=np.int)

