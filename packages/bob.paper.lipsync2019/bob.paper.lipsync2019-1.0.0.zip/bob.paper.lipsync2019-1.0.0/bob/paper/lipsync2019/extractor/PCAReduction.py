#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import bob.ip.base
import bob.ip.color
import os
import numpy
import math

from bob.bio.base.preprocessor import Preprocessor
from bob.bio.base.extractor import Extractor
import bob.bio.base.utils
import bob.learn.linear

from bob.paper.lipsync2019.utils import write_feature, read_feature

import bob.core
logger = bob.core.log.setup("bob.paper.lipsync2019")


class PCAReduction(Preprocessor, Extractor):
    """
    Computes optical flow on video frames.

    """

    def __init__(
            self,
            resulted_features_size=80,
            targeted_variance=None,
            per_modality_pca=False,
            limit_data=50000,
            list_of_feature_blocks=True,
            train_on_genuine_only=False,
            **kwargs
    ):
        Preprocessor.__init__(self, **kwargs)
        Extractor.__init__(self, requires_training=True,
                           split_training_data_by_client=train_on_genuine_only,
                           **kwargs)

        self.pca_machine = []
        self.resulted_features_size = resulted_features_size
        self.targeted_variance = targeted_variance
        self.per_modality_pca = per_modality_pca
        self.limit_data = limit_data
        # if true, then each feature is represented as list of blocks of features
        # This is used for LSTM-based processing, where temporal axis of the data is important
        self.list_of_feature_blocks = list_of_feature_blocks
        self.train_on_genuine_only = train_on_genuine_only

    def _train_pca(self, training_data):
        from bob.pad.voice.utils import extraction
        
        logger.info("Training PCA: shape of the training data %s" % str(training_data.shape))
        training_data = numpy.array( training_data, 'float64' )
        mean, std = extraction.calc_mean_std(training_data, nonStdZero=True)
        training_features = extraction.zeromean_unitvar_norm(training_data, mean, std)
        del training_data
        logger.info("Training PCA: shape of the training features %s" % str(training_features.shape))
        pca_trainer = bob.learn.linear.PCATrainer()
        pca_machine, eigenvalues = pca_trainer.train(training_features)
        del training_features
        # select only meaningful weights
        if self.targeted_variance is not None:
            cummulated = numpy.cumsum(eigenvalues) / numpy.sum(eigenvalues)
            for index in range(len(cummulated)):
                if cummulated[index] > self.targeted_variance:  # variance
                    break
            subspace_dimension = index
            logger.info("Found the features size to be %d for given variance %f" %
                        (subspace_dimension, self.targeted_variance))
        else:
            cummulated = numpy.cumsum(eigenvalues) / numpy.sum(eigenvalues)
            logger.info("The provided features size %d corresponds to variance %f " %
                        (self.resulted_features_size, cummulated[self.resulted_features_size]))
            subspace_dimension = self.resulted_features_size

        # import ipdb; ipdb.set_trace()

        # save the PCA matrix
        pca_machine.resize(pca_machine.shape[0], subspace_dimension)
        if mean is not None and std is not None:
            pca_machine.input_subtract = mean
            pca_machine.input_divide = std
        return pca_machine

    def _save_pca_model(self, pca_machine, hdf5file, pca_name='PCAProjector'):
        hdf5file.cd('/')
        hdf5file.create_group(pca_name)
        hdf5file.cd(pca_name)
        pca_machine.save(hdf5file)

    def _project_on_pca(self, feat):
        if self.per_modality_pca:
            projected_video = [self.pca_machine[0](f) for f in feat[0]]
            projected_audio = [self.pca_machine[1](f) for f in feat[1]]
            # return numpy.concatenate((projected_video, projected_audio), axis=1)
            return [projected_video, projected_audio]
        else:
            if isinstance(feat[0], list):  # two modalities are separated
                feat = numpy.concatenate(feat, axis=1)
            return [self.pca_machine[0](f.astype( 'float64' )) for f in feat]

    def train(self, training_data, extractor_file):
        # train separate PCA models for each modality
        hdf5file = bob.io.base.HDF5File(extractor_file, "w")
        if self.per_modality_pca:
            # limit the number of data points
            training_data = bob.bio.base.utils.selected_elements(training_data, self.limit_data)
            # collect video and audio features separately
            # video_feat = [[feat[0] for feat in groups] for groups in training_data]
            # video_feat = [[[vf for vf in feats[0]] for feats in groups] for groups in training_data]
            video_feat = []
            for groups in training_data:
                for video_audio in groups:
                    video_feat.append( video_audio[0] )  
            # video_feat = [feat[0] for feat in training_data]
            video_feat = numpy.concatenate(video_feat, axis=0)
            audio_feat = []
            for groups in training_data:
                for video_audio in groups:
                    audio_feat.append( video_audio[1] ) 
            # audio_feat = [feat[1] for feat in training_data]
            audio_feat = numpy.concatenate(audio_feat, axis=0)
            del training_data
            pca_machine = self._train_pca(video_feat)
            self.pca_machine += [pca_machine]
            self._save_pca_model(pca_machine, hdf5file, pca_name='PCAProjector_video')
            pca_machine = self._train_pca(audio_feat)
            self.pca_machine += [pca_machine]
            self._save_pca_model(pca_machine, hdf5file, pca_name='PCAProjector_audio')
        else:
            if self.train_on_genuine_only:
                # the data has two arrays [real, attacks], so we take only genuine data
                # the rest of the processing stays the same
                training_data = training_data[0]
            # combine all sets of features into one large matrix
            if isinstance(training_data[0], list):
                # if the data comes as list of lists (each file has a list of feature blocks)
                # we need to concatenate one more time
                # for i, data in enumerate(training_data):
                #     if len(data) > 1:
                # #         print("data {0} has {1} blocks".format(i, len(data)))
                training_data = [feature for data in training_data for feature in data]
            
            # limit the number of data points
            training_data = bob.bio.base.utils.selected_elements(training_data, self.limit_data)
            # import ipdb; ipdb.set_trace()
            if isinstance(training_data[0], list):
                feat = [numpy.concatenate(feat, axis=1) for feat in training_data]
                # feat.astype( int64 )
                del training_data
            else:
                # if audio and video are already concatenated in one vector, we are good
                feat = training_data
                del training_data
            feat = numpy.concatenate(feat, axis=0)
            pca_machine = self._train_pca(feat)
            self.pca_machine = [pca_machine]
            self._save_pca_model(pca_machine, hdf5file, pca_name='PCAProjector')

    def load(self, extractor_file):
        hdf5file = bob.io.base.HDF5File(extractor_file, "r")
        if self.per_modality_pca:
            hdf5file.cd('PCAProjector_video')
            self.pca_machine = [bob.learn.linear.Machine(hdf5file)]
            hdf5file.cd('/')
            hdf5file.cd('PCAProjector_audio')
            self.pca_machine += [bob.learn.linear.Machine(hdf5file)]
        else:
            hdf5file.cd('PCAProjector')
            self.pca_machine = [bob.learn.linear.Machine(hdf5file)]

    def write_feature(self, feature, feature_file):
        write_feature(feature, feature_file, concatenated_features=not self.per_modality_pca)

    def read_feature(self, feature_file):
        return read_feature(feature_file,
                            list_of_feature_blocks=self.list_of_feature_blocks,
                            concatenated_features=not self.per_modality_pca)

    def read_data(self, data_file):
        return self.read_feature(data_file)

    def __call__(self, input_data, annotations=None):
        """
            We assume that this class is not used as a true preporcessor but only to read the features
            so, if you call this method in preprocessor capacity, it will break
        """
        # we expect input_data to contain an array vector that PCA is able to reduce
        assert self.pca_machine
        if len(input_data) > 0:
            if isinstance(input_data[0], list):
                res_projections = []
                for data in input_data:
                    res_projections.append(self._project_on_pca(data))
                return res_projections
            return self._project_on_pca(input_data)

        return None
