"""
Template for the generic config file for SAVI. It should be used in combinaiton with other config files. [default: 0]

"""

import os
import numpy

import bob.io.base
from bob.paper.lipsync2019.utils.features_and_sets import sliding_windows, nonoverlapping_windows
data_extension = '.hdf5'

groups = ['{{ tfgroups }}']
# protocol = 'oneset'

shuffle = True


# 0 if it is tampered sample and 1 if it is original non-tampered one
def file_to_label(f):
    return int(f.attack_type is None)
    # return int(f.attack_type is not None)

# output = os.path.join(temp_dir, 'tf-records_' + sub_directory, 'lstm_{{ tfgroups }}_{{ tfwinsize }}-' + db_name)
network_size = {{tfarchitecure[1:]}}
output = os.path.join(temp_dir, 'tf-records_' + sub_directory, 'lstm_{{ tfgroups }}_{{ tfwinsize }}-' + db_name)

DATA_DIR = os.path.join(temp_dir, db_name)
if not os.path.exists(DATA_DIR):
    bob.io.base.create_directories_safe(DATA_DIR)
DATA_DIR = os.path.join(DATA_DIR, extracted_directory)

samples = database.objects(protocol=protocol, groups=groups) #, purposes=['real'] )
multiple_samples = True

allow_failures = True

#   window-size INT    The number of features in the output sample [default: 32].
window_size = {{ tfwinsize }}
#   sliding-step INT        The shifting step for the sliding window. By default, windows do not overlap.
sliding_step = {{ tfslidestep }}

if '{{ projectname }}' == 'face_autoenc_dual':
    extractor = AutoencoderReduction()

#   a, --sampling-attacks FLOAT  The portion of data that will be randomly sampled from attack
if '{{ tfgroups }}' == 'train':
    attacks_sampling = {{ tfattacksportion }}
else:
    # we write full samples into dev and eval tfrecords
    attacks_sampling = 0

def reader(padfile, per_modality_pca=False):
    # import ipdb; ipdb.set_trace()

    sample_path = padfile.make_path(DATA_DIR, data_extension)
    if os.path.exists(sample_path):
        # the extractor comes from the another piped config file
        data = extractor.read_feature(sample_path)
        label = file_to_label(padfile)
        key = padfile.path.encode()
        # we need to construct the windows of features (for LSTM)
        # from the continues blocks of data
        feature_windows = []

        # have we stored this as per modality
        if per_modality_pca:
            # the data is a list of feature blocks
            if not isinstance(data, list):
                data = [data]  # if it's not a list, we make it a list to unify processing
            for block in data:
                block = numpy.array( block )
                # get the video features first
                data_block = block[0,:,:]
                # concatenate in the audio along the 2nd dimension thus pcasize + pcasize
                data_block = numpy.concatenate( (data_block, block[1,:,:]), 1 )
                # make sure it's at least the size of our desired window
                if data_block.shape[0] < window_size:
                    continue
                # depending on the provided offset-length, split either in non-overlapping
                # windows or using sliding windows with provided offset-length
                if sliding_step:  # if offset is provided, do sliding windows
                    features = sliding_windows(data_block, window_size, sliding_step,
                                               label=label, random_sampling=attacks_sampling)
                else:  # non-overlapping windows
                    features = nonoverlapping_windows(data_block, window_size,
                                                      label=label, random_sampling=attacks_sampling)
                feature_windows.append(features) 
                
                if len(feature_windows) > 0:
                    feature_windows = numpy.vstack(feature_windows)
                    return (feature_windows, label, key)   
        else:    
            # the data is a list of feature blocks
            if not isinstance(data, list):
                data = [data]  # if it's not a list, we make it a list to unify processing
            for data_block in data:
                # one block must be smaller than the window size that will be fed into lstm
                data_block = data_block.astype(numpy.float32)
                if data_block.shape[0] < window_size:
                    continue
                # depending on the provided offset-length, split either in non-overlapping
                # windows or using sliding windows with provided offset-length
                if sliding_step:  # if offset is provided, do sliding windows
                    features = sliding_windows(data_block, window_size, sliding_step,
                                               label=label, random_sampling=attacks_sampling)
                else:  # non-overlapping windows
                    features = nonoverlapping_windows(data_block, window_size,
                                                      label=label, random_sampling=attacks_sampling)
                feature_windows.append(features)

            if len(feature_windows) > 0:
                feature_windows = numpy.vstack(feature_windows)
                return (feature_windows, label, key)

    return (None, None, None)


# def reader(padfile):
#     # import ipdb; ipdb.set_trace()
# 
#     sample_path = padfile.make_path(DATA_DIR, data_extension)
#     if os.path.exists(sample_path):
#         # the extractor comes from the another piped config file
#         data = extractor.read_feature(sample_path)
#         label = file_to_label(padfile)
#         key = padfile.path.encode()
# 
#         # we need to construct the windows of features (for LSTM)
#         # from the continues blocks of data
#         feature_windows = []
# 
#         # the data is a list of feature blocks
#         if not isinstance(data, list):
#             data = [data]  # if it's not a list, we make it a list to unify processing
#         for data_block in data:
#             # one block must be smaller than the window size that will be fed into lstm
#             data_block = data_block.astype(numpy.float32)
#             if data_block.shape[0] < window_size:
#                 continue
#             # depending on the provided offset-length, split either in non-overlapping
#             # windows or using sliding windows with provided offset-length
#             if sliding_step:  # if offset is provided, do sliding windows
#                 features = sliding_windows(data_block, window_size, sliding_step,
#                                            label=label, random_sampling=attacks_sampling)
#             else:  # non-overlapping windows
#                 features = nonoverlapping_windows(data_block, window_size,
#                                                   label=label, random_sampling=attacks_sampling)
#             feature_windows.append(features)
# 
#         if len(feature_windows) > 0:
#             feature_windows = numpy.vstack(feature_windows)
#             return (feature_windows, label, key)
# 
#     return (None, None, None)
