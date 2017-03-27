CONFIG = {
    'rows': 56,  # shift
    'columns': 16 + 3,  # multiplexer
    'min': 0,
    'max': 450,
    'serial': {
        'baud': 500000,
        'port': 'COM4'
    }
}

from heatmap.plot import main
