import sys

from heatmap import main

available_sources = ['fake', 'serial', 'replay']

if __name__ == '__main__':
    if len(sys.argv) > 1:
        data_source = sys.argv[1]
    else:
        data_source = 'fake'

    if data_source == 'fake':
        from heatmap.data_sources.fake_data import get_data
    elif data_source == 'ints' or data_source == 'serial':
        from heatmap.data_sources.read_ints import get_data
    elif data_source == 'replay':
        from heatmap.data_sources.replay import get_data
    else:
        raise KeyError('Invalid arguments. Valid arguments: %s' % (' '.join(available_sources), ))

    main(get_data)
