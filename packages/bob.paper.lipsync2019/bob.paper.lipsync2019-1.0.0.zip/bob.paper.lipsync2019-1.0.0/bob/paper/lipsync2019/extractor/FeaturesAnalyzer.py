#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os
import numpy

from bob.bio.base.preprocessor import Preprocessor
from bob.bio.base.extractor import Extractor

from bob.paper.lipsync2019.utils import read_feature

import bob.core
logger = bob.core.log.setup("bob.paper.lipsync2019")


class FeaturesAnalyzer(Preprocessor, Extractor):
    """
    Computes optical flow on video frames.

    """

    def __init__(
            self,
            output_file='features_stats',
            features_size=128,
            block_size = 1,
            list_of_feature_blocks=True,
            **kwargs
    ):
        Preprocessor.__init__(self, **kwargs)
        Extractor.__init__(self, requires_training=False,
                           split_training_data_by_client=False,
                           **kwargs)

        # if true, then each feature is represented as list of blocks of features
        # This is used for LSTM-based processing, where temporal axis of the data is important
        self.list_of_feature_blocks = list_of_feature_blocks
        self.text_logger = None
        self.output_file = output_file
        self.features_size = features_size
        self.block_size = block_size

    def write_feature(self, feature, feature_file):
        feature = numpy.asarray(feature, dtype=numpy.float16)
        filename, _ = os.path.splitext(os.path.basename(feature_file))
        numpy.set_printoptions(precision=4)
        if '-audio-' in filename:
            output_file = self.output_file + '_tampered.txt'
        else:
            output_file = self.output_file + '_non_tampered.txt'
        with open(output_file, 'a') as f:
            f.write('{0} '.format(filename))
            [f.write("{:0.6f} ".format(feat)) for feat in feature]
            f.write('\n')
        

    def read_feature(self, feature_file):
        return read_feature(feature_file,
                            list_of_feature_blocks=self.list_of_feature_blocks,
                            concatenated_features=True)

    def read_data(self, data_file):
        return self.read_feature(data_file)

    def __call__(self, input_data, annotations=None):
        """
            We assume that this class is not used as a true preporcessor but only to read the features
            so, if you call this method in preprocessor capacity, it will break
        """
        # we expect input_data to contain an array vector that PCA is able to reduce
        video_feat = []
        if len(input_data) > 0:
            if isinstance(input_data, list):
                for block in input_data:
                    for feat in block:
                        vid_features = feat[:self.features_size*self.block_size]
                        list_vid_features = numpy.split(vid_features, self.block_size)
                        for vfeat in list_vid_features:
                            video_feat.append(vfeat)  # video features
            else:
                for feat in input_data:
                    vid_features = feat[:self.features_size*self.block_size]
                    list_vid_features = numpy.split(vid_features, self.block_size)
                    for vfeat in list_vid_features:
                        video_feat.append(vfeat)  # video features
            video_feat = numpy.asarray(video_feat, dtype=numpy.float16)
            return numpy.std(video_feat, axis=0)

        return None
