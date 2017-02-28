import json

from serial import Serial
import numpy as np

from heatmap import CONFIG

COM_PORT = CONFIG.get('serial', {}).get('port', None)
BAUD_RATE = CONFIG.get('serial', {}).get('baud', None)

if COM_PORT is None or BAUD_RATE is None:
    raise KeyError('Baud rate and COM port must be specific in config to use serial communication.')

ser = Serial(COM_PORT, BAUD_RATE)


def get_data():
    line = ser.readline()
    data = json.loads(line)
    print(data)
    if 'error' in data:
        print('Error: %s' % data['error'])

    return np.asarray(data['data'], dtype=np.int)

