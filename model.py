import sys

available_commands = ['preview']

if __name__ == '__main__':
    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        command = None

    if command == 'preview':
        from ml.preview_all import main
        main()
    elif command == 'create':
        from ml.extract_data import create_train_and_test_data
        create_train_and_test_data()
    elif command == 'train':
        from ml.network import train
        train()
    else:
        raise KeyError('Invalid arguments. Valid arguments: %s' % (' '.join(available_commands),))

