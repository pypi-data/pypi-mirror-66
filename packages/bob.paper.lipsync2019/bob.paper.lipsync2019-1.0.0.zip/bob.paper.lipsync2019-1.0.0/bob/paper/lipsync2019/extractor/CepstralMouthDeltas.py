#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import bob.ip.base
import bob.ip.color
import os
import numpy
import math

from bob.bio.spear.extractor import CepstralExtended
from bob.bio.base.preprocessor import Preprocessor
from bob.paper.lipsync2019.utils import blockinize_feature_sets, find_continues_feature_sets, \
    one_audio_frame_for_each_video_frame, face_pose_yaw, write_feature, read_feature

import bob.core

logger = bob.core.log.setup("bob.paper.lipsync2019")


class CepstralMouthDeltas(Preprocessor, CepstralExtended):
    """
    Computes optical flow on video frames.

    """

    def __init__(
            self,
            win_length_ms=20.,  # 20 ms
            win_shift_ms=10.,  # 10 ms
            n_ceps=20,  # number of Cepstral features
            n_filters=20,  # number of Mel filters
            f_max=8000,  # maximum frequency that we consider
            pre_emphasis_coef=0.97,
            f_min=0,
            energy_filter=True,
            num_video_frames_per_block=5,
            video_frame_rate=25,
            delta_win=1,
            with_energy=False,  # compute energy coefficient
            take_video_features_asis=False,
            frame_dim=(720, 580),
            continuous_feature_blocks=False,
            min_feature_window_size=10,
            yaw_threshold=45,  # accept faces with yaws no more than 45 degrees
            concatenate_features=False,  # write/read features as separate audio/video channels or one block
            audio_context_instead_of_deltas = False,
            read_in_as_images=False,
            image_size=None,
            concat_sri_mfcc=False,
            **kwargs
    ):
        # call base class constructor with its set of parameters
        Preprocessor.__init__(self, **kwargs)
        CepstralExtended.__init__(self,
                                  win_length_ms=win_length_ms,
                                  win_shift_ms=win_shift_ms,
                                  with_energy=with_energy,
                                  keep_only_deltas=False,
                                  pre_emphasis_coef=pre_emphasis_coef,  # as per the algorithm implemented in the paper
                                  n_ceps=n_ceps,
                                  n_filters=n_filters,  # number of filters in the bank is also 20
                                  f_max=f_max,
                                  f_min=f_min,
                                  mel_scale=True,  # Mel-scaling is what make these MMFC features
                                  with_delta=True,  # As reported in the paper
                                  with_delta_delta=True,  # As reported in the paper
                                  energy_filter=energy_filter,  # The paper uses power of FFT magnitude
                                  dct_norm=True,  # The paper uses normed DCT-II variant
                                  delta_win=delta_win,  # the paper computes deltas on window of size 1
                                  **kwargs)

        self.num_video_frames_per_block = num_video_frames_per_block
        self.video_frame_rate = video_frame_rate
        # figure out how many audio frames for each video frame
        audio_frame_rate = 1000 // self.win_shift_ms  # each window is slides by win_shift_ms
        self.num_audioframes_per_videoframes = int(audio_frame_rate // self.video_frame_rate)
        self.take_video_features_asis = take_video_features_asis
        # how many audio frames fit within the time of one video frame
        self.num_audio_frames_per_block = self.num_video_frames_per_block * self.num_audioframes_per_videoframes
        self.frame_dim = frame_dim
        self.continuous_feature_blocks = continuous_feature_blocks
        self.min_feature_window_size = min_feature_window_size
        self.concatenate_features = concatenate_features
        self.audio_context_instead_of_deltas = audio_context_instead_of_deltas
        # are we reading in each visual component as a x*y image. This is for the dual auto encoder stuff.
        self.read_in_as_images = read_in_as_images
        # compute parameters for face pose estimation
        self.yaw_threshold = yaw_threshold / 100.0
        self.image_size = image_size
        self.concat_sri_mfcc = concat_sri_mfcc

    def write_feature(self, feature, feature_file):
        write_feature(feature, feature_file, concatenated_features=self.concatenate_features)

    def read_feature(self, feature_file):
        return read_feature(feature_file,
                            list_of_feature_blocks=True,
                            concatenated_features=self.concatenate_features)

    def read_data(self, data_file):
        """
        Read pre-computed audio-video features and return a joint one
        """
        # return the numpy array read from the data_file
        joint_features = self.read_feature(data_file)
        # import ipdb; ipdb.set_trace()
        # if we have a list of features
        if isinstance(joint_features[0], list):   
            all_features = []
            for joint_feat in joint_features:
                video_features = joint_feat[0]
                audio_features = joint_feat[1]
                assert (len(video_features) == len(audio_features))
                all_features.append([video_features, audio_features])   
            return all_features
        elif isinstance(joint_features, list) and self.concatenate_features:
            # features are in blocks each concatenated in a multimodal vector
            all_features = []
            for joint_feat in joint_features:
                all_features.append(joint_feat)   
            return all_features
        else: 
            video_features = joint_features[0]
            audio_features = joint_features[1]
            assert (len(video_features) == len(audio_features))
            # we keep features separate here, concatenate them at the next level
            # return numpy.concatenate((video_features, audio_features), axis=1)
            return [video_features, audio_features]

    def __call__(self, input_data, annotations=None):
        """
            We assume that this class is not used as a true preporcessor but only to read the features
            so, if you call this method in preprocessor capacity, it will break
        """
        pose_estimation = None
        pose = None
        audio_features = None
        audio_rate = None
        audio_data = None
        sri_senones = None # this is used when we are concatenating both together
        if self.concat_sri_mfcc:
            pose = input_data[0]
            video_features = input_data[1]
            pose_estimation = input_data[2]
            sri_senones = input_data[2]
            audio_rate = input_data[4]
            audio_data = input_data[5]
            speech_labels = input_data[6]
        else:
            if len(input_data) == 6:
                pose = input_data[0]
                video_features = input_data[1]
                pose_estimation = input_data[2]
                audio_rate = input_data[3]
                audio_data = input_data[4]
                speech_labels = input_data[5]
            elif len(input_data) == 5:
                # we expect video pose, video_features, pose_estimation, and audio_features. The last element it None
                pose = input_data[0]
                video_features = input_data[1]
                pose_estimation = input_data[2]
                audio_features = input_data[3]
            else:
                # we expect input_data to contain audio rate, audio data, audio labels, and video preprocessed features
                video_features = numpy.asarray(input_data[0], dtype=numpy.float64)
                audio_rate = input_data[1]
                audio_data = input_data[2]
                speech_labels = input_data[3]  # results of the VAD preprocessor

        # import ipdb;
        # ipdb.set_trace()
        # find MFCC features for audio frames
        if self.audio_context_instead_of_deltas:
            self.with_delta = False
            self.with_delta_delta = False

        # compute audio features if they were not passed from the previous step
        if audio_features is None:
            cepstral_coeff = self.compute_ceps(audio_rate, audio_data)
            cepstral_coeff = numpy.asarray(cepstral_coeff, dtype=numpy.float64)

            if self.audio_context_instead_of_deltas:
                # re-arange MFCC features, so each feature has its left and right neighbor as context
                # indices for middle features
                mid_ind = numpy.arange(len(cepstral_coeff))
                # indices for left features
                left_ind = mid_ind - 1
                left_ind[0] = left_ind[1]
                # indices for right features
                right_ind = mid_ind + 1
                right_ind[-1] = right_ind[-2]
                # insert left features in front of each middle feature
                audio_features = numpy.insert(cepstral_coeff, numpy.zeros(14), cepstral_coeff[left_ind], axis=1)
                # append right features at the end of each middle feature
                audio_features = numpy.append(audio_features, cepstral_coeff[right_ind], axis=1)
            else:
                audio_features = cepstral_coeff

        if sri_senones is not None:
            # create vectors of the same size
            min_val = numpy.min( (numpy.shape( audio_features )[0], numpy.shape( sri_senones )[0]) )
            audio_features = audio_features[:min_val]
            sri_senones = sri_senones[:min_val]
            # concatenate the two vectors
            audio_features = numpy.concatenate( (audio_features, sri_senones), axis=1 )
            
        video_features_length = video_features.shape[0]
        audio_features_length = audio_features.shape[0]

        # print("original audio_features_length", audio_features_length)
        # print("original video_features_length", video_features_length)
        if self.continuous_feature_blocks:
            if pose_estimation is not None:
                valid_indices = numpy.where(pose_estimation == 1.0)[0]
                if len(valid_indices) == 0 and numpy.all(pose[:,0]):  # take all of them anyway
                    valid_indices = numpy.where(pose_estimation == 0.0)[0]
            else:
                facial_yaws = [face_pose_yaw(landmarks, self.frame_dim) for landmarks in video_features]
                # make sure that we faces do not turn more than self.yaw_threshold
                valid_indices = numpy.where(numpy.abs(facial_yaws) < self.yaw_threshold)[0]


            valid_video_sets, valid_audio_sets = find_continues_feature_sets(valid_indices,
                                                                             video_features,
                                                                             audio_features,
                                                                             self.num_video_frames_per_block,
                                                                             self.num_audioframes_per_videoframes,
                                                                             read_as_image=self.read_in_as_images,
                                                                             image_size=self.image_size,)
        else:
            if self.num_video_frames_per_block == 1:
                video_features, audio_features = one_audio_frame_for_each_video_frame(video_features,
                                                                                      video_features_length,
                                                                                      audio_features,
                                                                                      audio_features_length,
                                                                                      self.num_audioframes_per_videoframes)
            # take all features as they are
            valid_video_sets = [video_features]
            valid_audio_sets = [audio_features]
        
        res_features = blockinize_feature_sets(valid_video_sets, valid_audio_sets,
                                               self.num_video_frames_per_block, self.num_audio_frames_per_block,
                                               self.take_video_features_asis, features_as_image_frame=self.read_in_as_images)
        # return the list of correct audio-visual blocks of features
        if len(res_features) == 0:
            return None
        return res_features
