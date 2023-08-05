#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import bob.ip.base
import bob.ip.color

from bob.bio.base.preprocessor import Preprocessor
# import bob.ip.optflow.liu
import numpy

from bob.paper.lipsync2019.utils import crop_mouth_from_landmarks

import bob.io.base
import bob.io.image
import cv2 # I am sure bob has one but I just need a resize image function and after a quick look I didn't see it.

import bob.core
import os

logger = bob.core.log.setup("bob.paper.lipsync2019")


###################### Temporary face register and rotate stuff #####################
import bob.bio.face
import bob.paper.lipsync2019

import time

class FaceNetMouthFeatures( Preprocessor ):
    """
    
    Computes the FaceNet features on video frames

    """
    
    # the initialiser
    def __init__(
            self,
            crop_height=128,
            crop_width=128,
            this_size=65,
            data_type="uint8",
            **kwargs
    ):
        Preprocessor.__init__( self, **kwargs )
        self.crop_width = crop_width
        self.crop_height = crop_height
        self.this_size = this_size

        self.data_type = "uint8"
        
        # Dim of output image
        self.crop_size = (self.crop_height, self.crop_width)

        # We place the mouth in the center
        self.mouth_center = (self.crop_height / 2, self.crop_width / 2)    
        
    def write_data(self, data, data_file, compression=0):
        f = bob.io.base.HDF5File( data_file, 'w' )
        f.set( "array", data, compression=compression )
        # print 'FaceNetMouthFeatures - datafile ', data_file, '\n'

    def read_data(self, data_file):
        # we assume the VAD for voice is already computed, so we read both
        # video and audio files
        # video file first
        f = bob.io.base.HDF5File(data_file)
        # pose = f.read("pose")
        # landmarks = f.read("landmarks")
        # pose_estimation = f.read("pose_estimation")
        video_array = f.read( "array" )
        # now, audio file
        hdf5_path, ext = os.path.splitext(data_file)
        hdf5_audio_path = hdf5_path + '-audio' + ext
        f = bob.io.base.HDF5File(hdf5_audio_path)
        audio_rate = f.read("rate")
        audio_data = f.read("data")
        audio_labels = f.read("labels")
        # return pose, landmarks, pose_estimation, audio_rate, audio_data, audio_labels
        return video_array, audio_rate, audio_data, audio_labels
    
    def __call__(self, video_frames, annotations=None):
        """
        __call__(frame_numbers, annotations = None) -> face

        """
        # print 'frames number : ', len( video_frames )
        # convert to the desired color channel in a numpy array
        # mouth_video = numpy.zeros((video_frames.shape[0],
        #                             video_frames.shape[1],
        #                             self.crop_height,
        #                             self.crop_width))

        # output in the OpeCV and Matplotlib format
        mouth_video = numpy.zeros((video_frames.shape[0],
                                   self.crop_height,
                                   self.crop_width,
                                   video_frames.shape[1]))

        logger.info( "Computing FaceNetMouthFeatures for %d frames " % (len( video_frames ), ) )

        # start timer
        start_time = time.time()
        #print 'All the annotation information : ', annotations
        for no_frame in range( len( video_frames ) ):
            rgb = video_frames[no_frame]
            # grey = bob.ip.color.rgb_to_gray( rgb )
            # does annotation exist?
            if str( no_frame ) in annotations.keys():
                lmks = annotations[str( no_frame )]["landmarks"]
                mouth_image = crop_mouth_from_landmarks( rgb,
                                                                   lmks,
                                                                   mouth_size = self.this_size,
                                                                   crop_size = (self.crop_height, self.crop_width),
                                                                   mouth_center = self.mouth_center )
                mouth_video[no_frame] = bob.io.image.to_matplotlib(mouth_image.astype(self.data_type))
            # else:
            #    lmks = None
            #print 'Landmarks of ', no_frame, ' : ', lmks

            # temporary playing around
            #bob.io.base.save( grey, 'grey.png' )
            #bob.io.base.save( video_frames[no_frame], 'rgb.png' )
        
        logger.info("Computing FaceNetMouthFeatures took %.2f seconds", (time.time() - start_time))
        return mouth_video 




# class that extracts the entire face rather than just the mouth region
class FaceNetFullFaceFeatures( Preprocessor ):
    """
    
    Computes the FaceNet features on video frames

    """
    
    # the initialiser
    def __init__(
            self,
            crop_height=160,
            crop_width=160,
            this_size=None,
            rotate_image='plain',
            **kwargs
    ):
        Preprocessor.__init__( self, **kwargs )
        self.crop_width = crop_width
        self.crop_height = crop_height
        self.this_size = this_size
        self.rotate_image = rotate_image
        # Dim of output image
        self.crop_size = (self.crop_height, self.crop_width)

        # We place the mouth in the center
        self.center = (self.crop_height / 2, self.crop_width / 2)
        
        ################### TEMPORARY #######################
        ######### To resize the image #######################
        self.faceregres = bob.paper.lipsync2019.preprocessor.VideoFaceCrop(
          face_cropper=bob.bio.face.preprocessor.FaceCrop(
              cropped_image_size=(crop_height, crop_width),
              # cropped_positions={'leye': (50, 97), 'reye': (50, 62)},
              cropped_positions={'lmth': (120, 112), 'rmth': (120, 48)},
              color_channel='rgb'),
          use_flandmark=True,
          color_channel='rgb',
          dtype='uint8'
         )

    def write_data(self, data, data_file, compression=0):
        f = bob.io.base.HDF5File( data_file, 'w' )
        f.set( "array", data, compression=compression )
        # print 'FaceNetMouthFeatures - datafile ', data_file, '\n'

    def read_data(self, data_file):
        # we assume the VAD for voice is already computed, so we read both
        # video and audio files
        # video file first
        f = bob.io.base.HDF5File(data_file)
        # pose = f.read("pose")
        # landmarks = f.read("landmarks")
        # pose_estimation = f.read("pose_estimation")
        video_array = f.read( "array" )
        # now, audio file
        hdf5_path, ext = os.path.splitext(data_file)
        hdf5_audio_path = hdf5_path + '-audio' + ext
        f = bob.io.base.HDF5File(hdf5_audio_path)
        audio_rate = f.read("rate")
        audio_data = f.read("data")
        audio_labels = f.read("labels")
        # return pose, landmarks, pose_estimation, audio_rate, audio_data, audio_labels
        return video_array, audio_rate, audio_data, audio_labels

    def _extract_with_rotation( self, frame, landmarks ):
        """
            rotates the face based on the landmark positions.
        """
        print ('FaceNetFullFaceFeatures _extract_with_rotation - empty function')
        
        t = time.time()
        m = time.localtime().tm_min
        s = time.localtime().tm_sec
        fn = os.path.join( '/idiap', 'temp', 'mhalstead', 'playing_around', 'rgb_%.05f_%d_%d.png' % (t, m, s) )
        
        return []
          

    def _extract_without_rotation( self, frame, landmarks ):
        """
            extracts process faces without rotation allowances.
            i.e. the face is in the same position it is in the raw footage.
        """
        # set up the variables at their extremes
        left = numpy.inf
        right = -numpy.inf
        top = numpy.inf
        bottom = -numpy.inf
        
        # search all the landmarks to get the extrema - this could be sped up with only certain landmarks in the future
        for l in landmarks:
            if l[0] > bottom:
                bottom = int( l[0] )
            if l[0] < top:
                top = int( l[0] )
            if l[1] < left:
                left = int( l[1] )
            if l[1] > right:
                right = int( l[1] )
        
        ## get the values to make sure the lengths of the axis are equal.    
        tb = bottom - top
        lr = right - left
        sz = tb if tb > lr else lr
        ctb = int( top + (tb / 2) )
        clr = int( left + (lr / 2) )
        new_top = int( ctb - (sz / 2) )
        new_bottom = int( new_top + sz )
        new_left = int( clr - (sz / 2) )
        new_right = int( new_left + sz )
        # create the square image of the right size.
        frame = frame[:, new_left:new_right, new_top:new_bottom]
        # now resize the rgb_pad image.- I am using opencv here, but I'm sure there is something in bob somewhere that wouldn't require the transposes to work.
        frame = numpy.transpose( cv2.resize( numpy.transpose( frame, (1,2,0) ), (self.crop_width, self.crop_height) ), (2,0,1) )
        
        return frame


    def __call__(self, video_frames, annotations=None):
        """
        __call__(frame_numbers, annotations = None) -> face

        """
        # convert to the desired color channel in a numpy array
        mouth_video = numpy.zeros((video_frames.shape[0],
                                    video_frames.shape[1],
                                    self.crop_height,
                                    self.crop_width))
                                                              
        for no_frame in range( 1 ):#len( video_frames ) ):
            rgb = video_frames[no_frame]
            # grey = bob.ip.color.rgb_to_gray( rgb )
            # does annotation exist?
            if str( no_frame ) in annotations.keys():
                lmks = annotations[str( no_frame )]["landmarks"]
                if self.rotate_image == 'plain':
                    mouth_video[no_frame] = self._extract_without_rotation( rgb, lmks )                        
                elif self.rotate_image == 'rotated':
                    # print 'FaceNetFeatures nothing in rotation of image'
                    mouth_video[no_frame] = self._extract_without_rotation( rgb, lmks )
                elif self.rotate_image == 'registered':
                    mouth_video[no_frame] = self.faceregres( rgb, lmks ) 
                    

        return mouth_video 

        # # TRIAL STUFF!!!!
        # rgb = video_frames[0]
        # # lmks = annotations[str( 0 )]["landmarks"]
        # t = time.time()
        # m = time.localtime().tm_min
        # s = time.localtime().tm_sec
        # fn = os.path.join( '/idiap', 'temp', 'mhalstead', 'playing_around', 'rgb_%.05f_%d_%d.png' % (t, m, s) )
        # bob.io.base.save( rgb, fn )
      

       