import struct
import time

from serial import Serial
import numpy as np

from heatmap import CONFIG

COM_PORT = CONFIG.get('serial', {}).get('port', None)
BAUD_RATE = CONFIG.get('serial', {}).get('baud', None)

rows = CONFIG.get('rows')
cols = CONFIG.get('columns')
indices = rows * cols
unpack_format = '>' + ('H' * indices)
num_bytes = 2 * rows * cols

if COM_PORT is None or BAUD_RATE is None:
    raise KeyError('Baud rate and COM port must be specific in config to use serial communication.')

ser = Serial(COM_PORT, BAUD_RATE)
time.sleep(5)

START_BYTE = bytearray([6])
EMPTY_ROW = np.zeros(cols, dtype=np.int)


def fix_data(data):
    """ Swap rows that have been rearranged

    :return:
    """
    data[8], data[54] = data[54], EMPTY_ROW
    return data


def get_data():
    while True:
        ser.write(START_BYTE)  # send start bit
        raw = ser.read(num_bytes)
        unpacked = struct.unpack(unpack_format, raw)
        data = np.reshape(np.asarray(unpacked, dtype=np.int), [rows, cols])

        yield fix_data(data)

