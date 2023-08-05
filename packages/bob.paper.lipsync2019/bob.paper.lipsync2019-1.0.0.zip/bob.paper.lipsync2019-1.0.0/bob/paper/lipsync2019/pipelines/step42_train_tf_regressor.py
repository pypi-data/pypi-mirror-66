
import os
import tensorflow as tf

from bob.learn.tensorflow.utils import reproducible
from bob.learn.tensorflow.loss import contrastive_loss
from bob.paper.lipsync2019.utils import lstm_regressor_input, Regressor, lstm_audio_to_video, Regressor_Contrastive, stacked_lstm_contrastive_regression
from bob.learn.tensorflow.dataset.tfrecords import batch_data_and_labels_image_augmentation, \
    shuffle_data_and_labels_image_augmentation

from functools import partial

# HYPER PARAMETERS
learning_rate = 0.0001

# other parameters
audio_cell = {{tfarchitecure[1]}} # used for lstm to 
video_cell = {{tfarchitecure[2]}} # used for lstm to 
stacked_lstm_cells = {{tfarchitecure[1:]}} # used for stacked lstm 
# audio_features = _audio_features_length # get from previous config file *** uncomment for the lstum to stuff
audio_features = _feature_length # taken from an earlier script step3
# video_features = _video_features_length # get from previous config file *** uncomment for the lstum to stuff
video_features = _feature_length # taken from an earlier script step3
num_time_steps = {{tfwinsize}}
network_size = {{tfarchitecure[1:]}}
# data_shape = [num_time_steps, video_features + 4 * audio_features] # *** uncomment for the lstum to stuff
data_shape = [num_time_steps, video_features + audio_features]
# Majik numbers
batch_size = 16
epochs = 150
data_type = tf.float32

# architecture
architecture = partial( stacked_lstm_contrastive_regression,
                        video_feature_length=video_features, # taken from an earlier script step3
                        cell_sizes=stacked_lstm_cells,
                        num_time_steps=num_time_steps,
                        batch_size=batch_size,
                      )

# architecture = partial( lstm_audio_to_video,
#                         audio_feature_length=audio_features, # 42
#                         video_feature_length=video_features, # 128
#                         audio_cell_size=audio_cell, # 16
#                         video_cell_size=video_cell, # 16
#                         num_time_steps=num_time_steps,
#                         batch_size=batch_size
#                       )
# architecture = partial( lstm_regressor_input,
#                         audio_feature_length=audio_features, # 42
#                         video_feature_length=video_features, # 128
#                         audio_cell_size=audio_cell, # 16
#                         video_cell_size=video_cell, # 16
#                         num_time_steps=num_time_steps,
#                         batch_size=batch_size
#                       )

# model location
model_dir = os.path.join(temp_dir, 'tf-models_' + sub_directory + '_lstm{0}'.format('_'.join(map(str, network_size))),
                         'mean_entropy_lr-{0}_epochs-{1}_vft_{2}_aft{3}_ws_{4}_lstm{5}'.format(
                             learning_rate, epochs, video_features, audio_features, num_time_steps, '_'.join(map(str, network_size))))

# Finding the tf records
tf_record_path = os.path.join(temp_dir, 'tf-records_' + sub_directory)
tfrecords_filename = [os.path.join(tf_record_path, f) for f in os.listdir(tf_record_path) if '_train' in f]
tfrecords_filename_validation = [os.path.join(tf_record_path, f) for f in os.listdir(tf_record_path) if '_dev' in f]

# some session preamble
session_config, run_config, _, _, _ = reproducible.set_seed()
run_config = run_config.replace(save_checkpoints_steps=1000)

# data collectors
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
    # return batch_data_and_labels_image_augmentation(tfrecords_filename, data_shape, data_type,
    #                                                 batch_size,
    #                                                 epochs=epochs,
    #                                                 output_shape=None,
    #                                                 buffer_size=10 * 4,
    #                                                 random_flip=False,
    #                                                 random_brightness=False,
    #                                                 random_contrast=False,
    #                                                 random_saturation=False,
    #                                                 random_rotate=False,
    #                                                 per_image_normalization=False,
    #                                                 gray_scale=False,
    #                                                 fixed_batch_size=True)


def eval_input_fn():
    return batch_data_and_labels_image_augmentation(tfrecords_filename_validation, data_shape, data_type,
                                                    batch_size,
                                                    epochs=1,
                                                    output_shape=None,
                                                    random_flip=False,
                                                    random_brightness=False,
                                                    random_contrast=False,
                                                    random_saturation=False,
                                                    per_image_normalization=False,
                                                    gray_scale=False,
                                                    fixed_batch_size=True)

# the optimizer
optimizer = tf.train.AdamOptimizer(learning_rate)

# the estimator
estimator = Regressor_Contrastive( architecture,
                                   optimizer=optimizer,
                                   # loss_op=tf.losses.mean_squared_error,
                                   loss_op=contrastive_loss,
                                   label_dimension=stacked_lstm_cells,
                                   config=run_config,
                                   model_dir=model_dir,
                                   apply_moving_averages=False,
                                   add_regularization_losses=False,
                                   extra_checkpoint=None,
                                   add_histograms=None
                                 )
# estimator = Regressor(  architecture,
#                         optimizer=optimizer,
#                         loss_op=tf.losses.mean_squared_error,
#                         label_dimension=[video_cell, audio_cell],
#                         config=run_config,
#                         model_dir=model_dir,
#                         apply_moving_averages=False,
#                         add_regularization_losses=False,
#                         extra_checkpoint=None,
#                         add_histograms=None
#                         )


