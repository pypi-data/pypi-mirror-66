
import tensorflow as tf

from bob.learn.tensorflow.dataset.tfrecords import create_dataset_from_records_with_augmentation


def shuffle_per_purposes_data_and_labels_image_augmentation(tfrecord_filenames,
                                               data_shape,
                                               data_type,
                                               batch_size,
                                               epochs=None,
                                               buffer_size=10**3,
                                               gray_scale=False,
                                               output_shape=None,
                                               random_flip=False,
                                               random_brightness=False,
                                               random_contrast=False,
                                               random_saturation=False,
                                               random_rotate=False,
                                               per_image_normalization=True,
                                               fixed_batch_size=False):
                                               
                                               
   # #
   # """ 
   #   This function will take multiple tf_record_filenames and create equal batches based on these records.
   # 
   #   **Parameters**
   # 
   #      tfrecord_filenames:
   #         List containing the tf-record paths - takes exactly 2 filenames
   # 
   #      data_shape:
   #         Samples shape saved in the tf-record
   # 
   #      data_type:
   #         tf data type(https://www.tensorflow.org/versions/r0.12/resources/dims_types#data_types)
   # 
   #      batch_size:
   #         Size of the batch - this will equally divide the tfrecord_filenames into the batch size. It checks that this is possible.
   # 
   #      epochs:
   #          Number of epochs to be batched
   # 
   #      buffer_size:
   #           Size of the shuffle bucket
   # 
   #      gray_scale:
   #         Convert to gray scale?
   # 
   #      output_shape:
   #         If set, will randomly crop the image given the output shape
   # 
   #      random_flip:
   #         Randomly flip an image horizontally  (https://www.tensorflow.org/api_docs/python/tf/image/random_flip_left_right)
   # 
   #      random_brightness:
   #          Adjust the brightness of an RGB image by a random factor (https://www.tensorflow.org/api_docs/python/tf/image/random_brightness)
   # 
   #      random_contrast:
   #          Adjust the contrast of an RGB image by a random factor (https://www.tensorflow.org/api_docs/python/tf/image/random_contrast)
   # 
   #      random_saturation:
   #          Adjust the saturation of an RGB image by a random factor (https://www.tensorflow.org/api_docs/python/tf/image/random_saturation)
   # 
   #      random_rotate:
   #          Randomly rotate face images between -5 and 5 degrees
   # 
   #     per_image_normalization:
   #          Linearly scales image to have zero mean and unit norm.
   # 
   #     fixed_batch_size:
   #          If True, the last remaining batch that has smaller size than `batch_size' will be dropped.
   # 
   # """
   
    # get the datasets
    dataset0 = create_dataset_from_records_with_augmentation(
                [tfrecord_filenames[0]],
                data_shape,
                data_type,
                gray_scale=gray_scale,
                output_shape=output_shape,
                random_flip=random_flip,
                random_brightness=random_brightness,
                random_contrast=random_contrast,
                random_saturation=random_saturation,
                random_rotate=random_rotate,
                per_image_normalization=per_image_normalization ) 
                
    #            
    dataset1 = create_dataset_from_records_with_augmentation(
                 [tfrecord_filenames[1]],
                 data_shape,
                 data_type,
                 gray_scale=gray_scale,
                 output_shape=output_shape,
                 random_flip=random_flip,
                 random_brightness=random_brightness,
                 random_contrast=random_contrast,
                 random_saturation=random_saturation,
                 random_rotate=random_rotate,
                 per_image_normalization=per_image_normalization )                 
    
    # first dataset                    
    dataset0 = dataset0.shuffle( buffer_size )
    if fixed_batch_size:
        dataset0 = dataset0.apply( tf.contrib.data.batch_and_drop_remainder( batch_size//2 ) )
    else:
        dataset0 = dataset0.batch( batch_size//2 )
    dataset0 = dataset0.repeat( epochs )
    
    d0, l0, k0 = dataset0.make_one_shot_iterator().get_next()
    
    # second dataset
    dataset1 = dataset1.shuffle( buffer_size )
    if fixed_batch_size:
        dataset1 = dataset1.apply( tf.contrib.data.batch_and_drop_remainder( batch_size//2 ) )
    else:
        dataset1 = dataset1.batch( batch_size//2 )
    dataset1 = dataset1.repeat( epochs )
    
    d1, l1, k1 = dataset1.make_one_shot_iterator().get_next()
    
    features = dict()
    features['data'] = tf.concat( (d0, d1), 0 )
    features['key'] = tf.concat( (k0, k1), 0 )
    labels = tf.concat( (l0, l1), 0 )
    
    return features, labels 