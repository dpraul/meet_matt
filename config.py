CONFIG = {
    'rows': 56,  # shift
    'columns': 16 + 3,  # multiplexer
    'min': 0,
    'max': 450,
    'serial': {
        'baud': 500000,
        'port': 'COM3'
    },
    'net': {
        'epochs': 50,
        'batch_size': 200,
        'dir': 'model'
    }
}