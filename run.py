import sys

from heatmap import main

available_sources = ['fake', 'serial']

if __name__ == '__main__':
    if len(sys.argv) > 1:
        data_source = sys.argv[1]
    else:
        data_source = 'fake'

    if data_source == 'fake':
        from heatmap.data_sources.fake_data import get_data
    elif data_source == 'serial':
        from heatmap.data_sources.read_serial import get_data
    else:
        raise KeyError('Invalid arguments. Valid arguments: %s' % (' '.join(available_sources), ))

    main(get_data)
