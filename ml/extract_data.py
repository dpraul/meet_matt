import os
import json
import random
import itertools

import numpy as np

DEFAULT_DATA_DIR = 'data'

flatten = lambda l: [item for sublist in l for item in sublist]


def get_samples(data_dir=DEFAULT_DATA_DIR):
    samples = {}
    filenames = {}

    for filename in os.listdir(data_dir):
        path = os.path.join(data_dir, filename)
        if not os.path.isfile(path):
            continue
        with open(path) as f:
            r = json.load(f)
        label = filename.split('_')[0]
        samples.setdefault(label, [])
        filenames.setdefault(label, [])

        sections = [int((len(r) - 1) / 2), ]
        if label in ('crunch', 'pushup'):  # grab part of the up AND down for crunch and pushup
            sections.append(sections[0] + 1)
        for section in sections:
            s = str(section)
            for i in np.linspace(0, len(r[s]), num=5, dtype=int)[1:-1]:  # grab three samples
                sample = r[s][i]['d']
                samples[label].append(sample)
                filenames[label].append('%s_%s_%s' % (filename, s, i))

    return samples, filenames


def create_train_and_test_data(data_dir=DEFAULT_DATA_DIR, validation_size=15):
    output_dir = os.path.join(data_dir, 'out')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    all_samples, _ = get_samples(data_dir)

    labels = {l: [1 if j == i else 0 for j in range(len(all_samples))]
              for i, l in enumerate(all_samples.keys())}

    with open(os.path.join(output_dir, 'labels.json'), 'w') as f:
        json.dump(labels, f)

    train = {'data': [], 'labels': []}
    test = {'data': [], 'labels': []}
    for label, samples in all_samples.items():
        test['data'].extend([flatten(samples.pop(random.randrange(len(samples)))) for _ in range(validation_size)])
        test['labels'].extend(itertools.repeat(labels[label], validation_size))
        train['data'].extend([flatten(s) for s in samples])
        train['labels'].extend(itertools.repeat(labels[label], len(samples)))

    with open(os.path.join(output_dir, 'train.json'), 'w') as f:
        json.dump(train, f)

    with open(os.path.join(output_dir, 'test.json'), 'w') as f:
        json.dump(test, f)


def get_train_and_test_data(output_dir=os.path.join(DEFAULT_DATA_DIR, 'out'), dtype=np.int16):
    with open(os.path.join(output_dir, 'train.json')) as f:
        train = json.load(f)

    with open(os.path.join(output_dir, 'test.json')) as f:
        test = json.load(f)

    return {
        'data': np.asarray(train['data'], dtype=dtype),
        'labels': np.asarray(train['labels'], dtype=dtype)
    }, {
        'data': np.asarray(test['data'], dtype=dtype),
        'labels': np.asarray(test['labels'], dtype=dtype)
    }


def get_labels(output_dir=os.path.join(DEFAULT_DATA_DIR, 'out')):
    with open(os.path.join(output_dir, 'labels.json')) as f:
        labels = json.load(f)

    l = {}
    for key, label in labels.items():
        l[np.argmax(label)] = key

    return l
