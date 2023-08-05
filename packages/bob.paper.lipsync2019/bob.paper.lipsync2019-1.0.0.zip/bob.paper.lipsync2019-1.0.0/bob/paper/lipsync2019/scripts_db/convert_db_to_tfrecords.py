#!/usr/bin/env python

"""Converts PAD datasets to TFRecords file formats.

Usage:
  %(prog)s [-v...] [options] [--] <config_files>...
  %(prog)s --help
  %(prog)s --version

Arguments:
  <config_files>  The config files.

Options:
  -h --help                         Show this help message and exit
  --version                         Show version and exit
  -v, --verbose                     Increases the output verbosity level
  -a, --allow-missing-files         Skips non-existing files of the database. [default: False]
  -o, --override-existing-record    Override tf-record file if exists. [default: True]


"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pkg_resources

import numpy
import bob.io.base
from bob.pad.base.database import PadDatabase

import tensorflow as tf
from bob.learn.tensorflow.utils.commandline import \
    get_from_config_or_commandline
# from bob.bio.base.utils.resources import read_config_file
from bob.extension.config import load as read_config_file

import bob.extension
import bob.core

logger = bob.core.log.setup("bob.paper.lipsync2019")


def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def nonoverlapping_windows(data, window_size, label=None, random_sampling=0.0):
    # find how many features (i.e., rows in the table) we have in the file
    num_splits = data.shape[0] // window_size
    num_features = num_splits * window_size
    data = data[:num_features]  # cut off the reminder
    windows = numpy.split(data, num_splits)
    windows = numpy.asarray(windows)

    # randomly sample the windows to return a required number of random windows
    # random_sampling is a portion of the windows to keep
    # label==0 for attacks or tampered features, so we only sample these
    if label == 0 and random_sampling > 0:
        sampled_indices = numpy.random.choice(num_splits, int(random_sampling * num_splits))
        windows = windows[sampled_indices]
    return windows


def sliding_windows(data, win_size, sliding_step, label=None, random_sampling=0.0):
    data_total_length = data.shape[0]
    data_row_size = data.shape[1]

    # compute the number of sliding windows
    num_win = int((data_total_length - win_size) / sliding_step) + 1

    # discard the tail of the features
    tail_size = (data_total_length - win_size) % sliding_step
    trimmed_length = data_total_length - tail_size
    data = data[:trimmed_length]

    # create strides
    from numpy.lib import stride_tricks
    # the resulted shape is
    # (number of windows, window size, size of each feature vector)
    # we assume each value of features is 4 bytes
    windows = stride_tricks.as_strided(data,
                                       shape=(num_win, win_size, data_row_size),
                                       strides=(data_row_size * 4, data_row_size * 4, 4))

    # randomly sample the windows to return a required number of random windows
    # random_sampling is a portion of the windows to keep
    # label==0 for attacks or tampered features, so we only sample these
    if label == 0 and random_sampling > 0:
        sampled_indices = numpy.random.choice(num_win, int(random_sampling * num_win))
        windows = windows[sampled_indices]
    return windows


def main(argv=None):
    from docopt import docopt
    import os
    import sys
    docs = __doc__ % {'prog': os.path.basename(sys.argv[0])}
    defaults = docopt(docs, argv=[""])
    args = docopt(docs, argv=argv, version="1.0.0")
    config_files = args['<config_files>']

    config = read_config_file(config_files)
    # config = bob.extension.config.load(config_files)

    # optional arguments
    verbosity = get_from_config_or_commandline(
        config, 'verbose', args, defaults)
    allow_missing_files = get_from_config_or_commandline(
        config, 'allow_missing_files', args, defaults)
    override_existing_record = get_from_config_or_commandline(
        config, 'override_existing_record', args, defaults)

    # Sets-up logging
    bob.core.log.set_verbosity_level(logger, verbosity)

    data_dir, output_file = config.DATA_DIR, config.TF_DB_FILE

    if not override_existing_record and os.path.exists(output_file):
        logger.warn("The tf-record file {} exists. Stopping tf-record creation, "
                    "since --override-existing-record is set to 'False'".format(output_file))
        return

    window_size = config.window_size
    sliding_step = config.sliding_step
    mean_std_filename = config.mean_std_filename
    attacks_sampling = config.attacks_sampling


    data_mean = None
    data_std = None
    # if the mean and std values are provided for us, use them later to normalize data
    if mean_std_filename and os.path.exists(mean_std_filename):
        npzfile = numpy.load(mean_std_filename)
        data_mean = npzfile['data_mean']
        data_std = npzfile['data_std']

    database, preprocessor = config.database, config.extractor
    database.protocol = config.protocol

    # Database directories, which should be automatically replaced
    if isinstance(database, PadDatabase):
        database.replace_directories(config.database_directories_file)

    files = database.objects(protocol=config.protocol, groups=config.groups)
    n_files = len(files)

    all_data = []
    all_labels = []
    all_data_coordinates = []
    total_num_samples = 0
    feature_size = 0
    global_data_index = 0
    with tf.python_io.TFRecordWriter(output_file) as writer:
        # collect features and corresponding labels into large numpy arrays
        for i, f in enumerate(files):
            path = f.make_path(data_dir, config.data_extension)
            if allow_missing_files and not os.path.exists(path):
                logger.warn("The path %s does not exist, skipping..." % path)
                continue

            # 1 if genuine and 0 if tampered
            label = int(f.attack_type is None)
            logger.info('Processing file %s, %d out of %d', path, i + 1, n_files)
            # logger.info('Saving data of size {0}'.format(data.shape))

            # read features form the file using given preprocessor
            data = preprocessor.read_data(path)

            # we want to accommodate data being a set of independent blocks
            if not isinstance(data, list):
                data = [data]  # if it's not a list, we make it a list to unify processing
            for data_block in data:
                if data_block.shape[0] < window_size:
                    continue
                if feature_size == 0:
                    feature_size = data_block.shape[1]
                all_data.append(data_block.astype('float32'))
                all_labels.append(label)  # label for each data sample
                # remember the place and size for each data sample
                # all_data_coordinates ordered the same way as labels, so we can correspond one with another
                all_data_coordinates.append((global_data_index, data_block.shape[0]))
                global_data_index += data_block.shape[0]

        # once we got all elements, convert to large uniform array
        # length of the row find from the last data point, assume here all rows are the same
        # all_data = numpy.reshape(numpy.vstack(all_data), newshape=[-1, feature_size])
        all_data = numpy.concatenate(all_data, axis=0)
        print(all_data.shape)
        # find and save mean and std to normalize the rows
        if data_mean is None or data_std is None:
            data_mean = numpy.mean(all_data, axis=0)
            data_std = numpy.std(all_data, axis=0)

        # mean should have the same size and each row in data samples
        assert (len(data_mean) == feature_size)

        # save mean and std in a file
        if not mean_std_filename or not os.path.exists(mean_std_filename):
            logger.info("Saving mean and std in file {0}:".format(mean_std_filename))
            bob.io.base.create_directories_safe(os.path.dirname(mean_std_filename))
            numpy.savez(mean_std_filename, data_mean=data_mean, data_std=data_std)

        # loop through labels (in randomized fashion) and
        # retrieve corresponding data samples so we can apply sliding windows
        randomized_indices = numpy.array(range(len(all_labels)))
        numpy.random.shuffle(randomized_indices)
        for index in randomized_indices:
            data_pos = all_data_coordinates[index][0]
            data_size = all_data_coordinates[index][1]
            # import ipdb; ipdb.set_trace()
            data = all_data[data_pos: data_pos + data_size]
            label = all_labels[index]
            #                print("label: ", label)
            #                print("sample: ", sample)
            #                logger.info('Saving data of size {0}'.format(sample.shape))

            # depending on the provided offset-length, split either in non-overlapping
            # windows or using sliding windows with provided offset-length
            if sliding_step:  # if offset is provided, do sliding windows
                features = sliding_windows(data, window_size, sliding_step,
                                           label=label, random_sampling=attacks_sampling)
            else:  # non-overlapping windows
                features = nonoverlapping_windows(data, window_size,
                                                  label=label, random_sampling=attacks_sampling)

            # normalize the features and save them to TF-records binary container
            features = numpy.asarray(numpy.divide(features - data_mean, data_std))
            for feature in features:
                total_num_samples += 1
                logger.info('Saving data of size {0} with label {1}'.format(feature.shape, label))
                feature = {'train/data': _bytes_feature(feature.tostring()),
                           'train/label': _int64_feature(label)
                           }

                example = tf.train.Example(features=tf.train.Features(feature=feature))
                writer.write(example.SerializeToString())

    logger.info("Total number of samples written: %d", total_num_samples)


if __name__ == '__main__':
    main()

