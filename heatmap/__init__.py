CONFIG = {
    'rows': 3,
    'columns': 3,
    'min': 0,
    'max': 700,
    'mux_delay': 10,  # ms
    'serial': {
        'baud': 115200,
        'port': 'COM4'
    }
}

from heatmap.plot import main
