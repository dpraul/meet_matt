from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os

import tensorflow as tf

from ml.extract_data import get_train_and_test_data, get_labels
from config import CONFIG

ROWS = CONFIG['rows']
COLS = CONFIG['columns']
NET_CONFIG = CONFIG['net']
LABELS = get_labels()
NUM_LABELS = len(LABELS)

if not os.path.exists(NET_CONFIG['dir']):
    os.makedirs(NET_CONFIG['dir'])

FLAGS = None


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


def build_session():
    # Create the model
    x = tf.placeholder(tf.float32, [None, ROWS * COLS])

    # first layer
    W_conv1 = weight_variable([5, 5, 1, 32])
    b_conv1 = bias_variable([32])

    x_image = tf.reshape(x, [-1, COLS, ROWS, 1])

    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    # second layer
    W_conv2 = weight_variable([5, 5, 32, 64])
    b_conv2 = bias_variable([64])

    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

    # densely connected layer
    W_fc1 = weight_variable([7 * 10 * 64, 1024])
    b_fc1 = bias_variable([1024])

    h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 10 * 64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    # dropout
    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    # readout layer
    W_fc2 = weight_variable([1024, NUM_LABELS])
    b_fc2 = bias_variable([NUM_LABELS])

    y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

    # Define loss and optimizer
    y_ = tf.placeholder(tf.float32, [None, NUM_LABELS])

    sess = tf.InteractiveSession()
    saver = tf.train.Saver()

    tf.global_variables_initializer().run()
    cross_entropy = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
    prediction = tf.argmax(y_conv, 1)
    correct_prediction = tf.equal(prediction, tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    sess.run(tf.global_variables_initializer())

    checkpoint = tf.train.get_checkpoint_state(NET_CONFIG['dir'])
    if len(sys.argv) > 2 and sys.argv[2] == 'r' and checkpoint and checkpoint.model_checkpoint_path:
        saver.restore(sess, checkpoint.model_checkpoint_path)  # restore all variables

    return sess, saver, train_step, prediction, accuracy, x, y_, keep_prob


def train():
    sess, saver, train_step, prediction, accuracy, x, y_, keep_prob = build_session()

    # Import data
    training, test = get_train_and_test_data()
    tr_x = training['data']
    tr_y = training['labels']

    batch_size = NET_CONFIG['batch_size']

    start = 0
    for i in range(start, NET_CONFIG['epochs']):
        j = 0
        for start, end in zip(range(0, len(tr_x), batch_size), range(batch_size, len(tr_x) + 1, batch_size)):
            train_accuracy = sess.run(accuracy, feed_dict={
                x: tr_x[start:end], y_: tr_y[start:end], keep_prob: 1.0})
            print("step %d.%d, training accuracy %g" % (i, j, train_accuracy))
            sess.run(train_step, feed_dict={x: tr_x[start:end], y_: tr_y[start:end], keep_prob: 0.5})
            j += 1

    saver.save(sess, '%s/%s' % (NET_CONFIG['dir'], "model.ckpt"))
    print("test accuracy %g" % sess.run(accuracy, feed_dict={
        x: test['data'], y_: test['labels'], keep_prob: 1.0}))


def get_predictor():
    sess, saver, train_step, prediction, accuracy, x, y_, keep_prob = build_session()

    return lambda xin: LABELS[sess.run(prediction, feed_dict={
        x: [xin.flatten()], keep_prob: 1.0
    })[0]]
