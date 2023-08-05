#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""
This preprocessor reads JSON-formatted files from OpenPose (pose and facial landmark detection), estimates the
rotation angle of the face, and saves it with landmarks to Bob formatted files.
It should be run after audio preprocessing is done.
"""

import bob.ip.base
import bob.ip.color

from bob.bio.base.preprocessor import Preprocessor
import numpy

import bob.core
import os
from bob.ip.tensorflow_extractor import MTCNN
from bob.ip.dlib import DlibLandmarkExtraction
import bob.ip.facedetect

logger = bob.core.log.setup("bob.paper.lipsync2019")

import time


class VideoMouthRegion(Preprocessor):
    """
    Computes optical flow on video frames.

    """

    def __init__(
            self,
            landmarks_range=(48, 68),
            external_audio_features_file=None,
            concat_sri_mfcc=False,
            **kwargs
    ):
        
        super(VideoMouthRegion, self).__init__(**kwargs)
        # Range of the mouth landmarks within the facial landmarks
        self.landmarks_range = landmarks_range
        self.external_audio_features_file = external_audio_features_file
        self.concat_sri_mfcc = concat_sri_mfcc
        self.face_detector = MTCNN()
        self.landmarks_extractor = DlibLandmarkExtraction()

    def write_data(self, data, data_file, compression=0):
        f = bob.io.base.HDF5File(data_file, 'w')
        f.set("pose", data[0], compression=compression)
        f.set("landmarks", data[1], compression=compression)
        f.set("pose_estimation", data[2], compression=compression)

    def _parse_tampered_names(self, data_file):
        original_spkn = data_file.split('/')[-2]
        if 'grid' == self.external_audio_features_file['db_name']:
            original_spkn = data_file.split('/')[-4]
        speaker_name, _ = os.path.splitext(data_file.split('-audio-')[1])  # remove extension
        original_smpn = os.path.split(data_file.split('-audio-')[0])[-1]
        with open(self.external_audio_features_file['tamper_mapping'], 'r') as tampered_mapping:
            lines = tampered_mapping.readlines()
            for line in lines:
                if '{0}:{1} {2}'.format(original_spkn, original_smpn, speaker_name) in line:
                    sample_name = line.strip().split(':')[-1]
                    break
        return speaker_name, sample_name

    def _parse_feature_path(self, data_file):
        speaker_name = data_file.split('/')[-2]
        if 'grid' == self.external_audio_features_file['db_name']:
            speaker_name = data_file.split('/')[-4]
        sample_name, _ = os.path.splitext(os.path.split(data_file)[-1])  # remove extension too
        return speaker_name, sample_name

    def _get_speaker_sample_names(self, data_file):
        if '-audio-' in data_file and 'tamper_mapping' in self.external_audio_features_file:
            # tampered file with a provided file of tampered mapping info
            speaker_name, sample_name = self._parse_tampered_names(data_file)
        else:
            # just extract both from the file path
            speaker_name, sample_name = self._parse_feature_path(data_file)
        if not speaker_name or not sample_name:
            raise ValueError('Wrongly formatted {0} file. Expected a text file with mappings for tampered '
                             'audio'.format(self.external_audio_features_file['tamper_mapping']))
        return speaker_name, sample_name

    def process_external_senone_features(self, data_file):
        # this is a little of a hack, for now, specific for VidTIMIT, Grid, or AMI databases
        # we expect a file with pre-extracted audio features for each speaker
        # or a folder with pre-extracted features for each speaker in HDF5 file
        if self.external_audio_features_file['features_type'] == 'dir_simple':
            # note that since we got here, senones are somewhere else, not in the usual preprocessed directory
#            import ipdb; ipdb.set_trace()
            hdf5_audio_path = data_file.split(self.external_audio_features_file['original_preprocess_dir'])[-1]
            hdf5_audio_path = self.external_audio_features_file['senones_dir'] + hdf5_audio_path
            hdf5 = bob.io.base.HDF5File(hdf5_audio_path)
            sample_name = self.external_audio_features_file['feature_name']

        elif self.external_audio_features_file['features_type'] == 'dir_samplename':
            # find the name of the speaker and the name of the sample that we need to read
            speaker_name, sample_name = self._get_speaker_sample_names(data_file)
            # when the features are stored in a separate file for each speaker
            hdf5 = bob.io.base.HDF5File(os.path.join(self.external_audio_features_file['senones_dir'],
                                                     speaker_name + '.hdf5'))

        elif self.external_audio_features_file['features_type'] == 'file':
            # find the name of the speaker and the name of the sample that we need to read
            speaker_name, sample_name = self._get_speaker_sample_names(data_file)
            # when the features are stored in one file with each speaker as a subgroup
            hdf5 = bob.io.base.HDF5File(self.external_audio_features_file['senones_db'])
            subgroups = hdf5.sub_groups(relative=True, recursive=False)
            if speaker_name not in subgroups:
                raise ValueError('Wrongly formatted {0} file. Expected an HDF5 file with features for speaker '
                                 '{1} and video {2}'.format(self.external_audio_features_file['senones_db'],
                                                            speaker_name, sample_name))
            hdf5.cd(speaker_name)
        else:
            raise ValueError('Not able to process the senones features, '
                             'the corresponding config "external_audio_features_file" is '
                             'invalid {}'.format(self.external_audio_features_file))

        return hdf5.read(sample_name)

    def _read_video_features(self, data_file):
        returned_values = ()
        hdf5 = bob.io.base.HDF5File(data_file)
        subgroups = hdf5.sub_groups(relative=True, recursive=False)
        # video data is written as a set of frames
        if len(subgroups) > 0:
            poses = []
            embeddings = []
            pose_estimations = []
            for path in subgroups:
              if path[:6] == 'Frame_':
                hdf5.cd(path)
                # Read data
                poses.append(hdf5.read("pose"))
                if "embedding" in hdf5:
                    embeddings.append(hdf5.read("embedding"))
                elif "image" in hdf5:
                    embeddings.append(hdf5.read("image"))
                pose_estimations.append(hdf5.read("pose_estimation"))

                hdf5.cd("..")
            returned_values += (numpy.vstack(poses), numpy.vstack(embeddings), numpy.vstack(pose_estimations))
            # print( 'VideoMouthRegion returned values', numpy.shape( returned_values[1] ) )
        else:
            pose = hdf5.read("pose")
            landmarks = hdf5.read("landmarks")
            pose_estimation = hdf5.read("pose_estimation")
            returned_values += (pose, landmarks, pose_estimation)

        return returned_values

    def _read_audio_features(self, data_file):
        audio_features = ()
        returned_values = (None,)
        if self.external_audio_features_file:
            # for instance, if we have pre-computed senone features
            audio_features = self.process_external_senone_features(data_file)
            audio_features = (audio_features,)  # make it a tuple for later use

        if self.concat_sri_mfcc or self.external_audio_features_file is None:
            # if these are just loaded up audio files
            hdf5_path, ext = os.path.splitext(data_file)
            hdf5_audio_path = hdf5_path + '-audio' + ext
            hdf5 = bob.io.base.HDF5File(hdf5_audio_path)
            audio_rate = hdf5.read("rate")
            audio_data = hdf5.read("data")
            audio_labels = hdf5.read("labels")
            returned_values = (audio_rate, audio_data, audio_labels)

        return audio_features + returned_values

    def read_data(self, data_file):
        # we assume the VAD for voice is already computed, so we read both
        # video and audio files
        # video file first
        returned_values = self._read_video_features(data_file)

        # now, process audio features
        returned_values += self._read_audio_features(data_file)

        return returned_values

    def estimate_pose(self, pose_confidence, lmks_confidence):
        # the order of pose: "Nose", "Neck", "REye", "LEye", "REar", "LEar"
        try:
            left_half_pose_confidence = numpy.mean([pose_confidence[3], pose_confidence[5]])
            right_half_pose_confidence = numpy.mean([pose_confidence[2], pose_confidence[4]])
        except Exception as e:
            raise Exception('Pose is wrongly extracted. '
                            'It should consist of 6 items but it is {}'.format(pose_confidence))

        # the order of the face landmarks:
        # https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/media/keypoints_face.png

        left_half_face_confidence = numpy.mean(numpy.concatenate([
            lmks_confidence[0:8],    # left chin
            lmks_confidence[17:22],  # left eye brow
            lmks_confidence[36:42],  # left eye
            lmks_confidence[31:33],  # left part of nose
            lmks_confidence[48:51],  # left part of mouth
            lmks_confidence[58:62],  # left part of mouth
            [lmks_confidence[67]]]     # left part of mouth
        ))
        right_half_face_confidence = numpy.mean(numpy.concatenate([
            lmks_confidence[9:17],   # right chin
            lmks_confidence[22:27],  # right eye brow
            lmks_confidence[42:48],  # right eye
            lmks_confidence[31:33],  # right part of nose
            lmks_confidence[52:57],  # right part of mouth
            lmks_confidence[63:66]]  # right part of mouth
        ))

        # STRICT FILTERING FOR FACES
#         # only one side of face is visible
#         strict_profile = (left_half_pose_confidence < 0.4 and right_half_pose_confidence > 0.4) or \
#                          (left_half_pose_confidence > 0.4 and right_half_pose_confidence < 0.4)
#
#         # the face is not frontal, as it is turned to a side but eyes are visible
# #        soft_profile = (left_half_pose_confidence > 0.5 and right_half_pose_confidence > 0.5) and \
#         soft_profile = (left_half_face_confidence < 0.5 and right_half_face_confidence > 0.5) or \
#                         (left_half_face_confidence > 0.5 and right_half_face_confidence < 0.5)
#
#         # this change is for submission to MedFor evaluation in May 2018
#         frontal = left_half_pose_confidence > 0.6 and right_half_pose_confidence > 0.6 and \
#                   left_half_face_confidence > 0.6 and right_half_face_confidence > 0.6
#
#         # frontal = left_half_pose_confidence > 0.4 and right_half_pose_confidence > 0.4 and \
#         #           left_half_face_confidence > 0.5 and right_half_face_confidence > 0.5
#
#         weak_face = left_half_pose_confidence > 0.4 and right_half_pose_confidence > 0.4 and \
#                     left_half_face_confidence > 0.0 and right_half_face_confidence > 0.0
#
#         if frontal:
#             return 1
#         if strict_profile:
#             return -1
#         if soft_profile:
#             return 2
#         if weak_face:
#             return 3

        # Non-STRICT FILTERING FOR FACES
        # only one side of face is visible
        strict_profile = (left_half_pose_confidence < 0.4 and right_half_pose_confidence > 0.4) or \
                         (left_half_pose_confidence > 0.4 and right_half_pose_confidence < 0.4)

        # the face is not frontal, as it is turned to a side but eyes are visible
        #        soft_profile = (left_half_pose_confidence > 0.5 and right_half_pose_confidence > 0.5) and \
        soft_profile = (left_half_face_confidence < 0.5 and right_half_face_confidence > 0.5) or \
                       (left_half_face_confidence > 0.5 and right_half_face_confidence < 0.5)

        frontal = left_half_pose_confidence > 0.4 and right_half_pose_confidence > 0.4 and \
                  left_half_face_confidence > 0.5 and right_half_face_confidence > 0.5

        if frontal:
            return 1
        if strict_profile:
            return -1
        if soft_profile:
            return 2

        # no face was detected
        return 0

    def compute_MTCNN_annotations(self, frames):
        annotations = {}
        for i, frame in enumerate(frames):
            boxes, scores, landmarks = self.face_detector.detect(frame)
            box = boxes[0]
            # 68 landmarks from Dlib
            lmks = self.landmarks_extractor(frame,
                                            bb=bob.ip.facedetect.BoundingBox((box[0], box[1]),
                                                                             (abs(box[0]-box[2]), abs(box[1]-box[3]))))
            lm = landmarks[0]  # we take only first face
            confidence = scores[0]
            # lmrks = [0] * 70  # fill the landmarks as much as we can from this inferior MTCNN model
            # lmrks[68] = [lm[0], lm[5]]  # right_eye
            # lmrks[69] = [lm[1], lm[6]]  # left_eye
            # lmrks[30] = [lm[2], lm[7]]  # nose
            # lmrks[48] = [lm[3], lm[8]]  # mouthright
            # lmrks[54] = [lm[4], lm[9]]  # mouthleft
            # lmrks[0] = [lm[0], box[1]]  # REar - the y as for the left eye but the x is for the box border
            # lmrks[16] = [lm[1], box[3]]  # LEar
            # lmrks[8] = [box[2], lm[7]]  # chin - the x as for nose and y as for box bottom
            pose = [0] * 6  # fill the landmarks as much as we can from this inferior MTCNN model
            pose[0] = [lm[2], lm[7]]  # nose
            pose[2] = [lm[0], lm[5]]  # right_eye
            pose[3] = [lm[1], lm[6]]  # left_eye
            pose[4] = [lm[0], box[1]]  # REar - the y as for the left eye but the x is for the box border
            pose[5] = [lm[1], box[3]]  # LEar
            pose[1] = [box[2], lm[7]]  # Neck - the x as for nose and y as for box bottom
            lmks_confidence = [confidence] * 68  # repeat the same score
            pose_confidence = [confidence] * 6
            annotations[str(i)] = {"landmarks": lmks,
                                   "landmarks_confidence": lmks_confidence,
                                   "pose": pose,
                                   "pose_confidence": pose_confidence}
        return annotations

    def __call__(self, frames, annotations=None):
        """__call__(frame_numbers, annotations = None) -> face

        """
        if not annotations:
            annotations = self.compute_MTCNN_annotations(frames)

        assert isinstance(annotations, dict)

        # import ipdb; ipdb.set_trace()
        if isinstance(frames, int):
            frames_number = frames
        elif isinstance(frames, numpy.ndarray):
            frames_number = frames.shape[0]
        else:  # this is a bob.io.video.reader then
            frames_number = frames.number_of_frames

        resulted_landmarks = numpy.zeros((frames_number, self.landmarks_range[1] - self.landmarks_range[0], 2))
        resulted_pose_estimation = numpy.zeros((frames_number, 1))
        resulted_pose_keypoints = numpy.zeros((frames_number, 6, 2))  # we have 6 pose keypoints

        logger.info("Computing requested landmarks for %d frames ", frames_number)
        non_empty_landmarks = 0
        for num_frame in range(frames_number):
            if str(num_frame) in annotations.keys():
                non_empty_landmarks += 1
                lmks = numpy.asarray(annotations[str(num_frame)]["landmarks"], dtype=numpy.float32)
                lmks_confidence = numpy.asarray(annotations[str(num_frame)]["landmarks_confidence"], dtype=numpy.float32)
                pose = numpy.asarray(annotations[str(num_frame)]["pose"], dtype=numpy.float32)
                pose_confidence = numpy.asarray(annotations[str(num_frame)]["pose_confidence"], dtype=numpy.float32)

                resulted_pose_estimation[num_frame] = self.estimate_pose(pose_confidence, lmks_confidence)
                resulted_landmarks[num_frame] = lmks[self.landmarks_range[0]: self.landmarks_range[1]]
                resulted_pose_keypoints[num_frame] = pose

        logger.info("Number of non-empty landmarks = %d", non_empty_landmarks)
        logger.info("Average pose estimation = %f", numpy.mean(resulted_pose_estimation))

        # return landmarks
        return resulted_pose_keypoints, resulted_landmarks, resulted_pose_estimation
