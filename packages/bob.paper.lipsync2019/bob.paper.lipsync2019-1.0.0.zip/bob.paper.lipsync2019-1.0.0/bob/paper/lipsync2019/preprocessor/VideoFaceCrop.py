#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""
This preprocessor reads JSON-formatted files from OpenPose (pose and facial landmark detection), and crops
videos using the detected right eye and left eye positions
"""
import random
import numpy
from bob.bio.face.preprocessor import FaceDetect
from bob.paper.lipsync2019.preprocessor import VideoMouthRegion


def read_data(hdf5, compute_landmarks=True):
    if compute_landmarks:
        pose = hdf5.read("pose")
        image = hdf5.read("image")
        pose_estimation = hdf5.read("pose_estimation")
        return pose, image, pose_estimation
    return hdf5.read("array")


class VideoFaceCrop(FaceDetect, VideoMouthRegion):
    """
    Computes optical flow on video frames.

    """

    def __init__(
            self,
            face_cropper,
            use_flandmark=False,
            landmarks_range=(48, 68),
            compute_landmarks=True,
            normalize_face=True,
            seed=None,
            # normalise_image=False,
            **kwargs
    ):
        # self.normalise_image = normalise_image
        FaceDetect.__init__(self, face_cropper=face_cropper,
                                                      use_flandmark=use_flandmark, **kwargs)
        VideoMouthRegion.__init__(self, landmarks_range, **kwargs)
        self.compute_landmarks = compute_landmarks
        self.normalize_face = normalize_face
        if seed is not None:
            random.seed(seed)

    @staticmethod
    def convert_to_crop_annotations(annotations):
        assert annotations is not None
        assert ('pose' in annotations and 'landmarks' in annotations)

        # the Openpose coordinates are (x, y) for each point
        # but Bob expects they to be (y, x)!!!
        crop_annotations = {
                  'reye' : (annotations['pose'][2][1], annotations['pose'][2][0]),
                  'leye' : (annotations['pose'][3][1], annotations['pose'][3][0]),
                  'rmth' : (annotations['landmarks'][48][1], annotations['landmarks'][48][0]), # this is actually the right mouth
                  'lmth' : (annotations['landmarks'][54][1], annotations['landmarks'][54][0]),  # this is actually the left mouth
                }
        return crop_annotations

    @staticmethod
    def compute_face_box(annotations, crop_annotations, image_shape=None):
        if not image_shape:
            image_shape = [3, 4096, 2160]  # the size of the UHD
        ## just return an estimated face bounding box
        # take the distance between the eyes and add smaller parts on two sides
        box_side = abs(crop_annotations['reye'][1] - crop_annotations['leye'][1])
        # 1.3 is just an intuitive number
        box_side = int(box_side / 1.3 + box_side + box_side / 1.3)
        # take the nose as the center of the face
        box_center = (annotations['pose'][0][1], annotations['pose'][0][0])
        # compute the top-left and bottom-right points of the bounding box
        tl_point = (min(int(box_center[0] + box_side / 2), image_shape[1]),
                    max(int(box_center[1] - box_side / 2), 0),)
        br_point = (max(int(box_center[0] - box_side / 2), 0),
                    min(int(box_center[1] + box_side / 2), image_shape[2]))
        return tl_point, br_point

    def crop_face(self, image, annotations=None):
        """crop_face(image, annotations = None) -> face

        Detects the face (and facial landmarks), and used the ``face_cropper`` given in the constructor to crop the face.

        **Parameters:**

        image : 2D or 3D :py:class:`numpy.ndarray`
          The face image to be processed.

        annotations :  Assumed that annotations are the landmarks from OpenPose

        **Returns:**

        face : 2D or 3D :py:class:`numpy.ndarray` (float)
          The detected and cropped face.
        """

        if not annotations:
            return None
        # get the eye landmarks
        crop_annotations = self.convert_to_crop_annotations(annotations)

        if self.normalize_face:
            # apply face cropping
            return self.cropper.crop_face(image, crop_annotations)
        else:
            tl_point, br_point = self.compute_face_box(annotations, crop_annotations, image.shape)
            im = image[:, br_point[0]: tl_point[0], tl_point[1]: br_point[1]]
            return im

    def write_data(self, data, data_file, compression=0):
        # f = bob.io.base.HDF5File(data_file, 'w')
        if self.compute_landmarks:
            data_file.set("pose", data[0], compression=compression)
            data_file.set("image", data[1], compression=compression)
            data_file.set("pose_estimation", data[2], compression=compression)
        else:
            data_file.set("array", data, compression=compression)

    def read_data(self, hdf5):
        # hdf5 = bob.io.base.HDF5File(data_file)
        return read_data(hdf5, self.compute_landmarks)

    def __call__(self, image, annotations=None):
        """__call__(image, annotations = None) -> face

        For each frame in a given video, aligns image according to the annotated face.

        For each frame, the desired color channel is extracted.
        Then, the face is detected and cropped, see :py:meth:`crop_face`.
        Finally, the resulting face is converted to the desired data type.

        **Parameters:**

        image : 2D or 3D :py:class:`numpy.ndarray`
          The video with face to be processed.

        annotations : Assumed annotations are provided by Openpose

        **Returns:**

        video faces : 4D :py:class:`numpy.ndarray`
          The video of cropped faces.
        """

        # convert to the desired color channel
        image = self.color_channel(image)

        # detect face and crop it
        image = self.crop_face(image, annotations=annotations)

        # # do we want to normalise the cropped image
        # if self.normalise_image:
        #     image = self._normalise_image( image )

        # convert data type
        image = self.data_type(image)

        # process the annotations
        if self.compute_landmarks and annotations is not None:
            # lmks = numpy.asarray(annotations["landmarks"], dtype=numpy.float32)
            pose = numpy.asarray(annotations["pose"], dtype=numpy.float32)
            lmks_confidence = numpy.asarray(annotations["landmarks_confidence"], dtype=numpy.float32)
            pose_confidence = numpy.asarray(annotations["pose_confidence"], dtype=numpy.float32)

            pose_estimation = self.estimate_pose(pose_confidence, lmks_confidence)
            if image is None and pose_estimation != 0:
                pose_estimation = 0  # no valid image region exists
                image = numpy.zeros(self.cropper.cropped_image_size, numpy.uint8)

            return pose, image, pose_estimation

        return image


class VideoNonFaceCrop(VideoFaceCrop):
    """
    Computes optical flow on video frames.

    """

    def __init__(
            self,
            face_cropper,
            **kwargs
    ):

        # random.seed(26)
        super(VideoNonFaceCrop, self).__init__(face_cropper=face_cropper, **kwargs)


    # @staticmethod
    # def intersection_area(rect1, rect2):  # returns None if rectangles don't intersect
    #     dx = min(rect1.xmax, rect2.xmax) - max(rect1.xmin, rect2.xmin)
    #     dy = min(rect1.ymax, rect2.ymax) - max(rect1.ymin, rect2.ymin)
    #     if (dx >= 0) and (dy >= 0):
    #         return dx * dy

    def crop_face(self, image, annotations=None):
        """crop_face(image, annotations = None) -> face

        Detects the face (and facial landmarks), and used the ``face_cropper`` given in the constructor to crop the face.

        **Parameters:**

        image : 2D or 3D :py:class:`numpy.ndarray`
          The face image to be processed.

        annotations :  Assumed that annotations are the landmarks from FaceNetFeatures

        **Returns:**

        face : 2D or 3D :py:class:`numpy.ndarray` (float)
          The detected and cropped face.
        """

        # import ipdb; ipdb.set_trace()
        if not annotations:
            return None

        # annotation_file = annotations['file']  # debugging hack
        # based on the crop annotations, crop a random region outside of the area
        crop_annotations = self.convert_to_crop_annotations(annotations)

        assert hasattr(self.cropper, 'cropped_keys')
        assert hasattr(self.cropper, 'cropped_positions')
        assert hasattr(self.cropper, 'cropped_image_size')
        # find region that we do not want to crop
        left_point = crop_annotations[self.cropper.cropped_keys[0]]
        right_point = crop_annotations[self.cropper.cropped_keys[1]]
        # the center of the whole annotation box, not the center between the cropping points
        # crop_center = ((left_point[0] + right_point[0]) / 2., (left_point[1] + right_point[1]) / 2.)
        lmks = numpy.asarray(annotations["landmarks"], dtype=numpy.float32)
        crop_center = ((max(lmks[:, 1]) + min(lmks[:, 1])) / 2.,
                       (max(lmks[:, 0]) + min(lmks[:, 0])) / 2.)
        # print('crop_center', crop_center)
        # relative distance from center to the points, it can be negative
        crop_dist_left_center = (crop_center[0] - left_point[0], crop_center[1] - left_point[1])
        crop_dist_right_center = (crop_center[0] - right_point[0], crop_center[1] - right_point[1])

        # distance between two points
        cropping_distance = abs(right_point[0] - left_point[0])
        target_cropping_distance = self.cropper.cropped_positions[self.cropper.cropped_keys[0]][0] - \
                                   self.cropper.cropped_positions[self.cropper.cropped_keys[1]][0]
        if target_cropping_distance == 0:
            cropping_distance = abs(right_point[1] - left_point[1])
            target_cropping_distance = self.cropper.cropped_positions[self.cropper.cropped_keys[0]][1] - \
                                       self.cropper.cropped_positions[self.cropper.cropped_keys[1]][1]
        # import ipdb; ipdb.set_trace()
        # compute the inplace cropping size
        # scale the cropped_image_size to find the inplace size
        scale_factor = 1. * cropping_distance / target_cropping_distance
        crop_size = (self.cropper.cropped_image_size[0] * scale_factor,
                     self.cropper.cropped_image_size[1] * scale_factor)

        crop_region = ((crop_center[0] - crop_size[0]*0.8 / 2, crop_center[0] + crop_size[0]*0.8 / 2),
                       (crop_center[1] - crop_size[1]*0.8 / 2, crop_center[1] + crop_size[1]*0.8 / 2))
        # print('crop_region', crop_region)
        # make search area for non-region a little smaller, so that we find less of an empty background
        safety_offset = 1.15
        small_x_border = crop_size[0] * (safety_offset - 1)
        large_x_border = image.shape[2] - crop_size[0] * safety_offset
        # large_x_border = image.shape[2] - image.shape[2] * 0.1
        small_y_border = crop_size[1] * (safety_offset - 1)
        large_y_border = image.shape[1] - crop_size[1] * safety_offset
        # large_y_border = image.shape[1] - image.shape[1] * 0.1
        # we use 4 overlapping rectangles around our crop region
        large_rects = [((small_x_border, crop_size[0] * safety_offset), (small_y_border, image.shape[2])),
                       ((small_x_border, image.shape[1]), (large_x_border, image.shape[2])),
                       ((large_y_border, image.shape[1]), (small_y_border, image.shape[2])),
                       ((small_x_border, image.shape[1]), (small_y_border, crop_size[1] * safety_offset))]
        # large_rects = [((0, crop_region[0][0]), (0, large_x_border)),
        #                ((0, large_y_border), (crop_region[1][1], large_x_border)),
        #                ((crop_region[0][1], large_y_border), (0, large_x_border)),
        #                ((0, large_y_border), (0, crop_region[1][0]))]
        rand_r = random.randint(0, 3)
        # selected a random rectangle from which we pick the non-region of the same size
        large_rect = large_rects[rand_r]
        # pick random bottom left coordinate and make sure the rectangle will be the same size as crop_size
        non_region_y = random.uniform(large_rect[0][0], large_rect[0][1] - crop_size[0])
        non_region_x = random.uniform(large_rect[1][0], large_rect[1][1] - crop_size[1])
        # import ipdb; ipdb.set_trace()

        non_region_center = (non_region_y + crop_size[0] / 2, non_region_x + crop_size[1] / 2)
        # print('crop-nonface-region', ((non_region_y, non_region_x), (non_region_y + crop_size[0], non_region_x + crop_size[1])))

        # place two fake points inside non-region in the same relative places they were in the original cropped region
        # use the relative distances from the center point computed earlier
        non_region_annotaitons = {
                          'reye' : (non_region_center[0]-crop_dist_right_center[0], non_region_center[1]-crop_dist_right_center[1]),
                          'leye' : (non_region_center[0]-crop_dist_left_center[0], non_region_center[1]-crop_dist_left_center[1]),
                          'rmth' : (non_region_center[0]-crop_dist_right_center[0], non_region_center[1]-crop_dist_right_center[1]),
                          'lmth' : (non_region_center[0]-crop_dist_left_center[0], non_region_center[1]-crop_dist_left_center[1]),
                        }
        # print(non_region_annotaitons)
        # return the found non-region resized into the expected size and shape
        return self.cropper.crop_face(image, non_region_annotaitons)
