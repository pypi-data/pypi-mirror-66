from bob.learn.tensorflow.dataset.tfrecords import batch_data_and_labels_image_augmentation
import os

import bob.bio.video

tfrecord_predict = tfrecords_filename + tfrecords_filename_validation

output_dir = os.path.join(model_dir, 'projections')

# uncommment if you want to use the best performing model on the development set
# checkpoint_path = os.path.join(model_dir, 'eval')

video_container = True

def predict_input_fn():
    return batch_data_and_labels_image_augmentation(tfrecord_predict, data_shape, data_type,
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

hooks = None