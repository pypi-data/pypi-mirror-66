#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import print_function

import numpy
import os
import bob.core

logger = bob.core.log.setup("bob.paper.lipsync2019")


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


def _write_one_feature(feature, hdf5file, concatenated_features=False, autoencoder_features=False):
    if concatenated_features:
        if isinstance(feature, list):
            if autoencoder_features:
                feature = numpy.reshape( feature, [-1,numpy.shape( feature )[2]] )
            else:
                feature = numpy.concatenate(feature, axis=1)
        hdf5file.set("array", feature, compression=False)
    else:
        video_features = feature[0]
        audio_features = feature[1]
        hdf5file.set("video", video_features, compression=False)
        hdf5file.set("audio", audio_features, compression=False)


def write_feature(feature, feature_file, concatenated_features=False, autoencoder_features=False):
    if feature is None or len(feature) == 0:
        logger.debug("write_feature(): "
                     "the extracted feature is None. Extraction file is not created.")
        return    
    hdf5file = bob.io.base.HDF5File(feature_file, "w")
    num_valid_features = 0
    if isinstance(feature, list):
        for feat, i in zip(feature, range(0, len(feature))):
            if feat is None or len(feat) == 0:
                continue  
            sub_group_name = "block_{:04d}".format(i)
            hdf5file.create_group(sub_group_name)
            hdf5file.cd(sub_group_name)
            _write_one_feature(feat, 
                               hdf5file, 
                               concatenated_features=concatenated_features, 
                               autoencoder_features=autoencoder_features, )
            hdf5file.cd("..")
            num_valid_features += 1
        if not num_valid_features:  # since the file is empty, remove it
            hdf5file.close()
            os.remove(feature_file)
    else:
        _write_one_feature(feature, hdf5file, concatenated_features)


def _read_one_feature(hdf5file, concatenated_features=False):
    if concatenated_features:
        return hdf5file.read("array")
    video_features = hdf5file.read("video")
    audio_features = hdf5file.read("audio")
    return [video_features, audio_features]


def read_feature(feature_file, list_of_feature_blocks=True, concatenated_features=False):
    # read audio-video features which are saved to the file
    hdf5file = bob.io.base.HDF5File(feature_file, "r")
    # if we are dealing with blocks of features saved in groups
    # if hdf5file.has_group('block_0000'):
    keys = [k for k in hdf5file.keys() if 'block_' in k]
    if len( keys ) > 0:
        features = []
        for sub_group in hdf5file.sub_groups():
            hdf5file.cd(sub_group)
            features.append(_read_one_feature(hdf5file, concatenated_features))
            hdf5file.cd("..")
        # return list of blocks of features
        if list_of_feature_blocks:
            return features
        else:
            # return the numpy array where all bocks are joined in one array
            return numpy.concatenate(features, axis=0)
    else:
        return _read_one_feature(hdf5file, concatenated_features)


def compute_mouth_deltas(mouth_lmks):
    """
    Compute distances between different mouth landmark points
    Args:
        mouth_lmks: 20 points of the mouth landmarks ordered as in this image:
        http://www.pyimagesearch.com/wp-content/uploads/2017/04/facial_landmarks_68markup.jpg

    Returns:
        42 deltas between landmark points: 14 vertical, 10 horizontal, 9 right-top diagonal, and
        9 left-bottom diagonal deltas.

    """

    deltas = numpy.zeros(42, dtype=numpy.float64)
    # vertical deltas, (5+3+3+3)=14 of them
    deltas[0:5] = numpy.linalg.norm(mouth_lmks[1:6] - mouth_lmks[11:6:-1], axis=1)
    deltas[5:8] = numpy.linalg.norm(mouth_lmks[13:16] - mouth_lmks[19:16:-1], axis=1)
    deltas[8:11] = numpy.linalg.norm(mouth_lmks[2:5] - mouth_lmks[19:16:-1], axis=1)
    deltas[11:14] = numpy.linalg.norm(mouth_lmks[13:16] - mouth_lmks[10:7:-1], axis=1)
    # horizontal deltas, (5+5)=10 of them
    deltas[14:17] = numpy.linalg.norm(mouth_lmks[0:3] - mouth_lmks[6:3:-1], axis=1)
    deltas[17:19] = numpy.linalg.norm(mouth_lmks[11:9:-1] - mouth_lmks[7:9], axis=1)
    deltas[19] = numpy.linalg.norm(mouth_lmks[0] - mouth_lmks[12])
    deltas[20] = numpy.linalg.norm(mouth_lmks[16] - mouth_lmks[6])
    deltas[21:23] = numpy.linalg.norm(mouth_lmks[13:11:-1] - mouth_lmks[15:17], axis=1)
    deltas[23] = numpy.linalg.norm(mouth_lmks[19] - mouth_lmks[17])
    # diagonal deltas, (5+5+4+4)=18 of them
    deltas[24] = numpy.linalg.norm(mouth_lmks[0] - mouth_lmks[2])
    deltas[25:29] = numpy.linalg.norm(mouth_lmks[8:12] - mouth_lmks[6:2:-1], axis=1)
    deltas[29:34] = numpy.linalg.norm(mouth_lmks[0:5] - mouth_lmks[10:5:-1], axis=1)
    deltas[34] = numpy.linalg.norm(mouth_lmks[12] - mouth_lmks[13])
    deltas[35:38] = numpy.linalg.norm(mouth_lmks[19:16:-1] - mouth_lmks[14:17], axis=1)
    deltas[38:42] = numpy.linalg.norm(mouth_lmks[12:16] - mouth_lmks[19:15:-1], axis=1)

    return deltas


def repeat_vframe_for_aframe(vindex, audioframes_per_videoframes, video_features, audio_features):
    for j in range(audioframes_per_videoframes):
        audio_feature_index = vindex * audioframes_per_videoframes + j
        audio_frame = audio_features[audio_feature_index]
        #                # skip all silent audio frames
        #                if not speech_labels[audio_feature_index]:
        #                    continue

        resulted_feature_vector = numpy.append(video_features, audio_frame)
        # normalize as the whole
        #                resulted_feature_vector = self.normalize_features(resulted_feature_vector)
        return resulted_feature_vector


def one_audio_frame_for_each_video_frame(video_features, video_features_length,
                                         audio_features, audio_features_length,
                                         num_audioframes_per_videoframes):
    # print("video_features_length", video_features_length)
    # print("audio_features_length", audio_features_length)
    # sometimes the length of audio and video are different, especially for tampered videos
    # hence, we take the common denominator
    video_features_length = min(video_features_length,
                                audio_features_length // num_audioframes_per_videoframes)
    audio_features_length = video_features_length * num_audioframes_per_videoframes

    # cut extra video features, if they are too many
    video_features = video_features[:video_features_length]
    # print("video_features_length", video_features_length)
    # print("audio_features_length", video_features_length * self.num_audioframes_per_videoframes)

    # for each video frame, we take the last corresponding audio frame
    # e.g., if of each video frame we have 4 audio frames, the audio indices should be [3, 7, 11, ...]
    audio_indices = numpy.array(range(num_audioframes_per_videoframes - 1,
                                      audio_features_length, num_audioframes_per_videoframes))
    print(audio_indices)
    audio_features = audio_features[audio_indices]
    # print("len audio_features", len(audio_features))
    # print("len video_features", len(video_features))
    return video_features, audio_features


def blocks_of_audio_video_frames(video_features, video_features_length, num_video_frames_per_block,
                                 audio_features, audio_features_length, num_audio_frames_per_block,
                                 features_as_image_frame):

    # how many whole blocks fit into current audio/video features
    num_audio_blocks = audio_features_length // num_audio_frames_per_block
    num_video_blocks = video_features_length // num_video_frames_per_block
    num_blocks = min(num_audio_blocks, num_video_blocks)
    if num_blocks == 0:
        return None
        
    # ignore features that are not fit into the whole number of blocks
    audio_features = audio_features[:num_blocks * num_audio_frames_per_block]
    video_features = video_features[:num_blocks * num_video_frames_per_block]

    # split audio and video features into blocks
    # audio
    audio_features = numpy.split(audio_features, num_blocks)
    audio_features = numpy.array([feature.flatten() for feature in audio_features])
    
    # videos
    if not features_as_image_frame:
        video_features = numpy.split(video_features, num_blocks, axis=0)
        video_features = numpy.array([feature.flatten() for feature in video_features])

    return [video_features, audio_features]


def remove_empty_rows(features):
    # find empty rows in the features
    zero_indices = numpy.where(~features.any(axis=1))[0]

    # for each empty row repeat the previous row
    features[zero_indices] = features[zero_indices - 1]
    return features


def find_continues_feature_sets(valid_indices, video_features, audio_features,
                                num_video_frames_per_block, num_audioframes_per_videoframes,
                                read_as_image=False, image_size=None):
    # if no valid visual detections, exit from here
    if not valid_indices.size:
        return [], []
    # find sets of consecutive valid indices
    # first, in valid_indices find the large enough gaps inside
    gaps_of_valid_indices = numpy.where(numpy.diff(valid_indices) > 1)[0]
    # split valid indices along those gaps and find chunks of continuous indices
    valid_chunks = numpy.split(valid_indices, gaps_of_valid_indices+1)
    # extract valid subsets of features
    if read_as_image:
        valid_video_sets = []
        for nogap_chunk in valid_chunks:
            video_set_chunk = []
            if image_size is not None:
                height = image_size[0]
            else:
                height = numpy.shape( video_features )[1] # the images are a square always.
            for i in nogap_chunk:
                start = i * height # numpy.shape( video_features )[1] # the images are a sqaure always.
                finish = (i+1) * height # numpy.shape( video_features )[1]
                video_set_chunk.append( video_features[start:finish, :] )
            valid_video_sets.append( video_set_chunk )    
        # 
    else:    
        valid_video_sets = [video_features[nogaps_chunk] for nogaps_chunk in valid_chunks]
    
    valid_audio_sets = [audio_features[
                        nogaps_chunk[0] * num_audioframes_per_videoframes:
                        (nogaps_chunk[-1]+1) * num_audioframes_per_videoframes]
                        for nogaps_chunk in valid_chunks]
                                            
    return valid_video_sets, valid_audio_sets


def blockinize_feature_sets(valid_video_sets, valid_audio_sets,
                            num_video_frames_per_block, num_audio_frames_per_block,
                            take_video_features_asis, features_as_image_frame=False):
    
    if valid_video_sets is None or len(valid_video_sets) == 0:
        return []

    res_features = []
    # we have sets of features
    for video_set, audio_set in zip(valid_video_sets, valid_audio_sets):
        # make sure that each set of features is large enough to fit a window of blocks
        # needed for LSTM training
        if len(video_set) >= num_video_frames_per_block and \
                len(audio_set) >= num_audio_frames_per_block:
            
            if not take_video_features_asis:
                video_set = numpy.array(
                    [compute_mouth_deltas(face_lmks[48:68]) for face_lmks in video_set])
            feature_block = blocks_of_audio_video_frames(video_set, len(video_set),
                                                         num_video_frames_per_block,
                                                         audio_set, len(audio_set),
                                                         num_audio_frames_per_block,
                                                         features_as_image_frame)
                                                         
            if feature_block is None or feature_block[0] is None or \
                    len(feature_block[0]) == 0:
                logger.debug("blockinize_feature_sets(): feature block is invalid or too small, so dropping it!")
            else:
                res_features.append(feature_block)
                    
    return res_features
