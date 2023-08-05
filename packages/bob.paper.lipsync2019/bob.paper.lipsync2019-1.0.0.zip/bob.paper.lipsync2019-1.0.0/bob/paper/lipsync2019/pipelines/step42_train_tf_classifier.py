from bob.learn.tensorflow.estimators import Logits
from bob.learn.tensorflow.loss import mean_cross_entropy_loss
from bob.learn.tensorflow.dataset.tfrecords import batch_data_and_labels_image_augmentation, \
    shuffle_data_and_labels_image_augmentation
from bob.learn.tensorflow.utils.hooks import LoggerHookEstimator
from bob.learn.tensorflow.utils import reproducible
import os
import tensorflow as tf

from bob.paper.lipsync2019.utils import stacked_lstm, audio_video_separate_lstm, lstm_dimreduction_stacked_lstm

slim = tf.contrib.slim

from functools import partial

# HYPER PARAMETERS
learning_rate = 0.001
embedding_validation = False

n_classes = 2
data_type = tf.float32
feature_size = _feature_length  # get the feature size from the previous config file
num_time_steps = {{tfwinsize}}
sliding_win_len = {{tfwinsize}}
sliding_win_step = {{tfwinsize}}
batch_size = {{tfbatchsize}}
validation_batch_size = {{tfbatchsize}}
network_size = {{tfarchitecure[1:]}}
architecture_name = '{{ tfarchitecure[0] }}'

epochs = 50

eval_interval_secs = 20

data_shape = [num_time_steps, feature_size]
output_shape = None


# architecture = partial(
#     audio_video_separate_lstm,
#     video_features_length=_block_size * _video_features_length,
#     batch_size=batch_size,
#     cell_sizes=network_size,
#     num_time_steps=num_time_steps)

#architecture = partial(
#    lstm_dimreduction_stacked_lstm,
#    block_size = _block_size,
#    video_features_length=_block_size * _video_features_length,
#    batch_size=batch_size,
#    cell_sizes=network_size,
#    num_time_steps=num_time_steps)

architecture = partial(
    stacked_lstm,
    batch_size=batch_size,
    cell_sizes=network_size,
    activation=tf.nn.tanh,
    num_time_steps=num_time_steps,)

model_dir = os.path.join(temp_dir, 'tf-models_' + sub_directory + '_lstm{0}'.format('_'.join(map(str, network_size))),
                         'mean_entropy_lr-{0}_epochs-{1}_ft_{2}_ws_{3}_lstm{4}_batch{5}'.format(
                             learning_rate, epochs, feature_size, sliding_win_len,
                             '_'.join(map(str, network_size)), batch_size))

# Finding the tf records
tf_record_path = os.path.join(temp_dir, 'tf-records_' + sub_directory)
tfrecords_filename = [os.path.join(tf_record_path, f) for f in os.listdir(tf_record_path) if '_train' in f]
tfrecords_filename_validation = [os.path.join(tf_record_path, f) for f in os.listdir(tf_record_path) if '_dev' in f]


def train_input_fn():
    return shuffle_data_and_labels_image_augmentation(tfrecords_filename, data_shape, data_type, batch_size,
                                                      epochs=epochs,
                                                      output_shape=None,
                                                      buffer_size=10 * 4,
                                                      random_flip=False,
                                                      random_brightness=False,
                                                      random_contrast=False,
                                                      random_saturation=False,
                                                      random_rotate=False,
                                                      per_image_normalization=False,
                                                      gray_scale=False,
                                                      fixed_batch_size=True)


def eval_input_fn():
    return batch_data_and_labels_image_augmentation(tfrecords_filename_validation, data_shape, data_type,
                                                    validation_batch_size,
                                                    epochs=1,
                                                    output_shape=None,
                                                    random_flip=False,
                                                    random_brightness=False,
                                                    random_contrast=False,
                                                    random_saturation=False,
                                                    per_image_normalization=False,
                                                    gray_scale=False,
                                                    fixed_batch_size=True)

# If more than 0, will keep the best N models in the evaluation folder
keep_n_best_models = 1
# The metric for sorting the N best evaluated models.
sort_by = 'accuracy'

session_config, run_config, _, _, _ = reproducible.set_seed()
run_config = run_config.replace(save_checkpoints_steps=1000, keep_checkpoint_max=30)

optimizer = tf.train.AdamOptimizer(learning_rate)
estimator = Logits(model_dir=model_dir,
                   architecture=architecture,
                   loss_op=mean_cross_entropy_loss,
                   optimizer=optimizer,
                   n_classes=n_classes,
                   embedding_validation=embedding_validation,
                   validation_batch_size=validation_batch_size,
                   config=run_config,
                   apply_moving_averages=False)

# from tensorflow.python import debug as tf_debug
# hooks = [tf_debug.LocalCLIDebugHook()]


hooks = [LoggerHookEstimator(estimator, batch_size, 300),
         tf.train.SummarySaverHook(save_steps=300,
                                   output_dir=model_dir,
                                   scaffold=tf.train.Scaffold(),
                                   summary_writer=tf.summary.FileWriter(model_dir))]
