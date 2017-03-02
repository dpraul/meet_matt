CONFIG = {
    'rows': 8,
    'columns': 16,
    'min': 0,
    'max': 450,
    'mux_delay': 10,  # ms
    'serial': {
        'baud': 115200,
        'port': 'COM4'
    }
}

from heatmap.plot import main
