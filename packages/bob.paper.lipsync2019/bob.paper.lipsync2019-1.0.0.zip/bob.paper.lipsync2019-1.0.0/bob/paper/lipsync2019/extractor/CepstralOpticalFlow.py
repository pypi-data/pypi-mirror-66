#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import bob.ip.base
import bob.ip.color
import os
import numpy
import math

from bob.bio.spear.extractor import CepstralExtended

import bob.core
logger = bob.core.log.setup("bob.paper.lipsync2019")


class CepstralOpticalFlow(CepstralExtended):
    """
    Computes optical flow on video frames.

    """

    def __init__(
            self,
            win_length_ms=20.,  # 20 ms
            win_shift_ms=10.,  # 10 ms
            histogram_bins=60,
            **kwargs
    ):
        CepstralExtended.__init__(self,
                                  win_length_ms=win_length_ms,
                                  win_shift_ms=win_shift_ms,
                                  keep_only_deltas=False,
                                  pre_emphasis_coef=0.97,  # as per the algorithm implemented in the paper
                                  n_ceps=20,
                                  n_filters=20,  # number of filters in the bank is also 20
                                  f_max=8000,
                                  mel_scale=True,  # Mel-scaling is what make these MMFC features
                                  with_delta=True,  # As reported in the paper
                                  with_delta_delta=True,  # As reported in the paper
                                  energy_filter=True,  # The paper uses power of FFT magnitude
                                  dct_norm=True,  # The paper uses normed DCT-II variant
                                  delta_win=1,  # the paper computes deltas on window of size 1
                                  **kwargs)
        self.histogram_bins = histogram_bins

    def compute_histogram(self, frame):
        # computing flow orientation field (FOF)
        th = numpy.arctan2(frame[1, :, :], frame[0, :, :])
        th = numpy.where(th < -math.pi, th + (2 * math.pi), th)
        # compute histogram of FOF
        histogram = bob.ip.base.histogram(th, (-math.pi, math.pi), self.histogram_bins)
        # print("histogram ", histogram)
        histogram = histogram.astype('float64')
        # normalize histogram
        # histogram /= numpy.linalg.norm(histogram)
        # histogram /= histogram.sum()
        # print("normalized ", histogram)
        # print(th.shape)
        return histogram

    def __call__(self, input_data, annotations=None):
        """__call__(data, annotations = None) -> face

        """
        # we expect input_data to contain audio rate, audio data, audio labels, and video preprocessed features
        video_optical_flows = numpy.asarray(input_data[0], dtype=numpy.float64)
        audio_rate = input_data[1]
        audio_data = input_data[2]
        speech_labels = input_data[3] # results of the VAD preprocessor

        # find MFCC features for audio frames
        cepstral_coeff = self.compute_ceps(audio_rate, audio_data)
        cepstral_coeff = numpy.asarray(cepstral_coeff, dtype=numpy.float64)
        # normalize audio features
        # cepstral_coeff = self.normalize_features(cepstral_coeff)
        # cepstral_coeff = numpy.reshape(cepstral_coeff, (speech_labels.shape[0], -1))

        video_features_length = video_optical_flows.shape[0]
        audio_features_length = cepstral_coeff.shape[0]

        # sometimes video features are longer than audio features
        # so, we have to follow audio to figure out how many video frames to
        # take
        audio_sec = len(audio_data) * 1.0 / audio_rate
        video_features_length = int(audio_sec * 25) - 1  #  25 is video frame rate

        size_of_video_feature = self.histogram_bins
        size_of_audio_feature = cepstral_coeff.shape[1]

        # how many audio frames fit within the time of one video frame
        audioframes_per_videoframes = int(round(audio_features_length / video_features_length))

        # we ignore the trailing audio frames here, since we don't know which video frame to repeat for them
        resulted_features = numpy.zeros((audioframes_per_videoframes * video_features_length,
                                         size_of_video_feature + size_of_audio_feature))

        print(video_features_length, audio_features_length, audioframes_per_videoframes)
        for i, video_frame in zip(range(video_features_length), video_optical_flows):
            # if the frame is empty, ignore it
            if not numpy.count_nonzero(video_frame):
                continue
            # compute histogram for this frame
            frame_histogram = self.compute_histogram(video_frame)
            # normalize histogram
            # frame_histogram = self.normalize_features(frame_histogram)
            for j in range(audioframes_per_videoframes):
                audio_feature_index = i * audioframes_per_videoframes + j
                audio_frame = cepstral_coeff[audio_feature_index]
                resulted_feature_vector = numpy.append(frame_histogram, audio_frame)
                # normalize as the whole
                resulted_feature_vector = self.normalize_features(resulted_feature_vector)
                resulted_features[audio_feature_index] = resulted_feature_vector

        # remove empty features here
        mask = resulted_features == 0
        rows = numpy.flatnonzero((~mask).sum(axis=1))
        resulted_features = resulted_features[rows.min():rows.max() + 1, :]

        return resulted_features
