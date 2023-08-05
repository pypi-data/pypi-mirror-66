#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import bob.ip.base
import bob.ip.color
import os
import numpy
import math

from bob.bio.spear.extractor import CepstralExtended
from bob.bio.base.preprocessor import Preprocessor

import bob.core

# for extracting the nn features.
import bob.bio.video
from bob.ip.tensorflow_extractor import FaceNet
from bob.bio.base.extractor import Extractor



logger = bob.core.log.setup("bob.paper.lipsync2019")

# instance of the extractor class.
class FacenetExtractor(FaceNet, Extractor):
    pass

# full feature extractor.
class FaceNetRegionExtractor( Preprocessor, CepstralExtended ):
    """
    Computes facenet features on video frames and links with the audio component.

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
            #take_video_features_asis=False,
            frame_dim=(128, 128),
            for_frontal_faces_only=False,
            min_feature_window_size=10,
            yaw_threshold=45,  # accept faces with yaws no more than 45 degrees
            overlapping_blocks=False, # are we overlapping the feature blocks in a sliding window fashion or are we non-overlapping (by default)
            **kwargs ):
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
        # get the video data.
        self.num_video_frames_per_block = num_video_frames_per_block
        self.video_frame_rate = video_frame_rate  
        self.frame_dim = frame_dim                                        
        # figure out how many audio frames for each video frame
        audio_frame_rate = 1000 // self.win_shift_ms  # each window is slides by win_shift_ms
        self.num_audioframes_per_videoframes = int(audio_frame_rate // self.video_frame_rate)
        #self.take_video_features_asis = take_video_features_asis
        # how many audio frames fit within the time of one video frame
        self.num_audio_frames_per_block = self.num_video_frames_per_block * self.num_audioframes_per_videoframes
        self.frame_dim = frame_dim
        self.for_frontal_faces_only = for_frontal_faces_only
        self.min_feature_window_size = min_feature_window_size
        
        # create the video extractor
        self.facenet_extractor = bob.bio.video.extractor.Wrapper(FacenetExtractor( image_size=self.frame_dim[0] ),
                                                    frame_selector=bob.bio.video.FrameSelector(selection_style='all'))
        # are we overlapping the video and audio blocks in a sliding window fashion or non overlapping
        self.overlapping_blocks=overlapping_blocks                                            
    
    
    def write_feature(self, feature, feature_file):
        if feature is None or len(feature) == 0:
            logger.debug("FaceNetMouthExtractor::write_feature(): "
                         "the extracted feature is None. Extraction file is not created.")
            return
        hdf5file = bob.io.base.HDF5File(feature_file, "w")
        num_valid_features = 0
        # print 'FaceNetMouthExtractor::write_feature - feature type : ', type( feature )
        # print 'FaceNetMouthExtractor::write_feature - feature len : ', len( feature )
        # print 'FaceNetMouthExtractor::write_feature - frontal faces only : ', self.continuous_feature_blocks
        if self.for_frontal_faces_only and isinstance(feature, list):
            # print 'FaceNetMouthExtractor::write_feature using frontal faces only'
            for feat, i in zip(feature, range(0, len(feature))):
                if feat is None:
                    continue
                sub_group_name = "block_{:04d}".format(i)
                hdf5file.create_group(sub_group_name)
                hdf5file.cd(sub_group_name)
                self._write_one_feature_block(feat, hdf5file)
                hdf5file.cd("..")
                num_valid_features += 1
            if not num_valid_features:  # since the file is empty, remove it
                hdf5file.close()
                os.remove(feature_file)
        else:
            # print 'FaceNetMouthExtractor::write_feature not using frontal faces only'
            self._write_one_feature_block(feature, hdf5file)


    def _write_one_feature_block(self, feature, hdf5file):
        video_features = feature[0]
        audio_features = feature[1]

        hdf5file.set("video", video_features, compression=False)
        hdf5file.set("audio", audio_features, compression=False)


    def _read_one_feature_block(self, hdf5file):
        video_features = hdf5file.read("video")
        audio_features = hdf5file.read("audio")
        return [[video_features, audio_features]]


    def read_feature(self, feature_file):
        # read audio-video features which are saved to the file
        hdf5file = bob.io.base.HDF5File(feature_file, "r")
        # if we are dealing with blocks of features saved in groups
        if self.for_frontal_faces_only or hdf5file.has_group('block_0000'):
            # print 'FaceNetMouthExtractor.py::read_features inside self.continuous_feature_blocks'
            features = []
            for sub_group in hdf5file.sub_groups():
                hdf5file.cd(sub_group)
                features.append(self._read_one_feature_block(hdf5file))
                hdf5file.cd("..")
            # return list of blocks of features
            return features
        else:
            # print 'FaceNetMouthExtractor.py::read_features not inside self.continuous_feature_blocks'
            return self._read_one_feature_block(hdf5file)


    def read_data(self, data_file):
        """
        Read pre-computed audio-video features and return a joint one
        """
        # return the numpy array read from the data_file
        joint_features = self.read_feature(data_file)
        # if we have a list of features
        if isinstance(joint_features[0], list):
            all_features = []
            for joint_feat in joint_features:
                video_features = joint_feat[0]
                audio_features = joint_feat[1]
                assert (len(video_features) == len(audio_features))
                all_features.append([video_features, audio_features])
            return all_features
        else:
            video_features = joint_features[0]
            audio_features = joint_features[1]
            assert (len(video_features) == len(audio_features))
            # we keep features separate here, concatenate them at the next level
            # return numpy.concatenate((video_features, audio_features), axis=1)
            return [video_features, audio_features]
                
        
    def _compute_facenet_features( self, 
                                   video_features ):
        """
        computes the facenet features from the video / images
        """                           
        fc = self._create_frame_container( video_features )
        return self.facenet_extractor( fc ).as_array()
        
    def _create_frame_container( self, 
                                 video_features ):
        """
        Because my input is a numpy array and the created FacenetExtractor requires a specific frame container I convert it here.
        """                         
        framecontainer = bob.bio.video.utils.FrameContainer()
        for frame_id, vf in enumerate( video_features ):
            framecontainer.add( frame_id, vf )
            
        return framecontainer       


    def _blocks_of_audio_video_frames( self, 
                                       video_features,
                                       audio_features ):
                                       
        """
        Based on the input features, extract the appropriate number of features from each.
        Flatten them then concatenate them.
        """                                   
        video_features_length = video_features.shape[0]
        audio_features_length = audio_features.shape[0]   
        # print '_blocks_of_audio_video_frames video size : ', video_features_length
        # print '_blocks_of_audio_video_frames audio size : ', audio_features_length         
        # print '_blocks_of_audio_video_frames video type : ', type( video_features_length )
        # print '_blocks_of_audio_video_frames audio type : ', type( audio_features_length )                           
        # how many whole blocks fit into current audio/video features
        num_audio_blocks = audio_features_length // self.num_audio_frames_per_block
        num_video_blocks = video_features_length // self.num_video_frames_per_block
        num_blocks = min(num_audio_blocks, num_video_blocks)
        if num_blocks == 0:
            return None

        # ignore features that are not fit into the whole number of blocks
        audio_features = audio_features[:num_blocks * self.num_audio_frames_per_block]
        video_features = video_features[:num_blocks * self.num_video_frames_per_block]
        
        # split audio and video features into blocks
        audio_features = numpy.split(audio_features, num_blocks)
        video_features = numpy.split(video_features, num_blocks)
        # print '_blocks_of_audio_video_frames video type after split : ', type( video_features_length )
        # print '_blocks_of_audio_video_frames audio type after split : ', type( audio_features_length )
        # print("_blocks_of_audio_video_frames shape audio_features", numpy.shape( audio_features ) )
        # print("_blocks_of_audio_video_frames shape video_features", numpy.shape( video_features ) ) 

        # concatenate each block into vector and re-arrange them together in matrix
        audio_features = numpy.array([feature.flatten() for feature in audio_features])
        video_features = numpy.array([feature.flatten() for feature in video_features])
        # print '_blocks_of_audio_video_frames video type after flat : ', type( video_features_length )
        # print '_blocks_of_audio_video_frames audio type after flat : ', type( audio_features_length )
        # print("FaceNetMouthExtract _blocks_of_audio_video_frames shape audio_features flat", audio_features.shape)
        # print("FaceNetMouthExtract _blocks_of_audio_video_frames shape video_features flat", video_features.shape)  
        # print("FaceNetMouthExtract _blocks_of_audio_video_frames shape concat features flat", numpy.shape( [video_features, audio_features] ) )      
        return [video_features, audio_features]                         
    
        
    def __call__( self, 
                  input_data, 
                  annotations=None ):
        """
            We assume that this class is not used as a true preporcessor but only to read the features
            so, if you call this method in preprocessor capacity, it will break
        """
        
        # we expect input_data to contain audio rate, audio data, audio labels, and video preprocessed features
        video_features = numpy.asarray( input_data[0], dtype=numpy.float64 )
        audio_rate = input_data[1]
        audio_data = input_data[2]
        speech_labels = input_data[3]  # results of the VAD preprocessor                               
        
        # import ipdb; ipdb.set_trace()
        # find MFCC features for audio frames
        cepstral_coeff = self.compute_ceps( audio_rate, audio_data )
        audio_features = numpy.asarray( cepstral_coeff, dtype=numpy.float64 )
        # print 'FaceNetMouthExtractor __call__ shape of audio features : ', numpy.shape( audio_features )
        # remove first MFCC coefficient
        # audio_features = cepstral_coeff[:, 1:]
        # audio_features = cepstral_coeff
        video_features_length = video_features.shape[0]
        audio_features_length = audio_features.shape[0]   
        
        if self.num_video_frames_per_block == 1:
            #return self.one_audio_frame_for_each_video_frame(video_features, video_features_length,
            #                                                 audio_features, audio_features_length)
            print( 'FaceNetMouthExtract.py one frame of video does nothing at this stage.' )
        else:  
            if self.for_frontal_faces_only:
                print( 'FaceNetMouthExtract.py frontal faces only does nothing at this stage.' ) 
                
                                
            else:
                # we are using the entire list of indices because we are assuing always frontal.
                valid_indices = range( video_features_length )
                
                # I assume that the video features are based on the FacenNet pre-processor. N*C*I*J
                # calculate the video cnn features based on the input video features and the pre-trained facenet model 
                video_vgg_features = self._compute_facenet_features( video_features )
                
                # output the concatenated feature vectors.
                return self._blocks_of_audio_video_frames( video_vgg_features, audio_features )