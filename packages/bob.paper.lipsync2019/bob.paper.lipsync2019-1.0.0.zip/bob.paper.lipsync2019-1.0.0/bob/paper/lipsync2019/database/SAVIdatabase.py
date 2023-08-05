#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>

from bob.pad.base.database import PadFile
from bob.pad.base.database import FileListPadDatabase, HighBioDatabase

from bob.bio.base.database import FileListBioDatabase
from bob.bio.base.database.file import BioFile

import bob.bio.video

import bob.io.base
# must import here if we want to read videos (even if we would use bob.io.base.load() method)
# loading bob.io.video registers video file formats with bob
import bob.io.video

import numpy
import scipy
import os
import json
from tempfile import TemporaryDirectory


def _iter_annotation_files(annotations_path):
    # import ipdb; ipdb.set_trace()
    for filename in sorted(os.listdir(annotations_path)):
        if not filename.endswith('.json'):
            continue
        frame_id = int(filename.split('_')[-2])
        # print (frame_id)
        # print type( frame_id )
        # assume one face per video
        with open(os.path.join(annotations_path, filename), 'r') as f:
            yield frame_id, json.load(f)


def unzip_annotations(filename):
    import tarfile
    ext = os.path.splitext(filename)[-1].lower()
    if ext == ".zip":
        raise ValueError('Annotations are not supported as Zip files')

    if ext in [".bz2" or ".tbz2"]:
        mode = "r:bz2"
    elif ext in [".gz" or ".tgz"]:
        mode = "r:gz"
    else:
        mode = "r"

    with TemporaryDirectory(prefix='openpose_annotations_') as temp_dir:
        with tarfile.open(name=filename, mode=mode) as t:
            t.extractall(temp_dir)
            basename = os.path.split(os.path.splitext(filename)[0])[1]
            if basename.endswith(".tar"):
                basename = os.path.splitext(basename)[0]
            json_dir = os.path.join(temp_dir, basename)
            if not os.path.exists(json_dir):
                raise ValueError("The annotation directory {} does not exist".format(json_dir))
            for frame_id, json in _iter_annotation_files(json_dir):
                yield frame_id, json


def _iter_annotations(original_directory, annotation_file):
    if isinstance(annotation_file, str):
        annotations_path = annotation_file
    else:
        annotations_path = annotation_file.make_path(original_directory, '')
        if annotation_file.is_tampered():
            annotations_path = annotation_file.path_non_tampered_version(original_directory, '')
    if not os.path.exists(annotations_path):
        # may be annotations are compressed in a file
        supported_compressions = [".bz2", ".tbz2", ".gz", ".tgz", ".tar", ".tar.gz"]
        for compression_ext in supported_compressions:
            if os.path.exists(annotations_path+compression_ext):
                return unzip_annotations(annotations_path+compression_ext)
            yield None, None # we will need to run MTCNN to find annotations
    return _iter_annotation_files(annotations_path)


def _annotations(original_directory, annotation_file):
    """
    Parses the JSON formatted output of OpenPose detector:
    https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/output.md
    For the pose, we are interested in 0, 1, 14, 15, 16, and 17 points:
    // POSE_COCO_BODY_PARTS {
    //     {0,  "Nose"},
    //     {1,  "Neck"},
    //     {2,  "RShoulder"},
    //     {3,  "RElbow"},
    //     {4,  "RWrist"},
    //     {5,  "LShoulder"},
    //     {6,  "LElbow"},
    //     {7,  "LWrist"},
    //     {8,  "RHip"},
    //     {9,  "RKnee"},
    //     {10, "RAnkle"},
    //     {11, "LHip"},
    //     {12, "LKnee"},
    //     {13, "LAnkle"},
    //     {14, "REye"},
    //     {15, "LEye"},
    //     {16, "REar"},
    //     {17, "LEar"},
    //     {18, "Background"},
    // }
    In keypoints v2, the indexes are 0, 1, 15, 16, 17, and 18 instead
    Returns:
        Dictionary of annotations, including pose and facial landmarks with detection confidences

    """
    # import ipdb; ipdb.set_trace()
    # check if we get a file path or file object
    annotations = {}
    for frame_id, annotations_json in _iter_annotations(original_directory, annotation_file):
        if frame_id is None:
            return annotations
        # if more than one person, select the one with the largest confidence
        chosen_index = 0
        json_version = 1
        if len(annotations_json['people']) > 0:
            if 'face_keypoints_2d' in annotations_json['people'][0].keys():
                json_version = 2
            people_confidence = []
            for person in annotations_json['people']:
                if json_version == 1:
                    people_confidence.append(numpy.mean(person['face_keypoints'][2::3]))
                else:
                    people_confidence.append(numpy.mean(person['face_keypoints_2d'][2::3]))
            chosen_index = numpy.argmax(people_confidence)
        else:  # no people were detected
            continue
        chosen_one = annotations_json['people'][chosen_index]
        if json_version == 1:
            pose_keypoints = chosen_one['pose_keypoints']
            # we are interested in the keypoints for nose, neck, eyes, and ears
            pose = pose_keypoints[0:6] + pose_keypoints[14 * 3:18 * 3]
        else:
            # for keypoints v2, the default models is BODY 25, so
            # nose, neck, eyes, and earts correspond to points 0, 1, 15, 16, 17, and 18
            pose_keypoints = chosen_one['pose_keypoints_2d']
            if len(pose_keypoints) == 54:
                # keypoints v1 - old 2018 model
                pose = pose_keypoints[0:6] + pose_keypoints[14 * 3:18 * 3]
            else:
                # keypoints v2
                pose = pose_keypoints[0:6] + pose_keypoints[15 * 3:19 * 3]

        pose_confidence = pose[2::3]
        pose_x = pose[0::3]
        pose_y = pose[1::3]

        if json_version == 1:
            face_keypoints = chosen_one['face_keypoints']
        else:
            face_keypoints = chosen_one['face_keypoints_2d']

        face_confidence = face_keypoints[2::3]
        face_x = face_keypoints[0::3]
        face_y = face_keypoints[1::3]

        # skip empty faces
        if numpy.mean(face_keypoints) == 0 or numpy.mean(face_confidence) < 0.0001:
            continue

        annotations[frame_id] = {}
        annotations[frame_id]['pose_confidence'] = pose_confidence
        annotations[frame_id]['pose'] = [[x, y] for x, y in zip(pose_x, pose_y)]
        annotations[frame_id]['landmarks_confidence'] = face_confidence
        annotations[frame_id]['landmarks'] = [[x, y] for x, y in zip(face_x, face_y)]
    return annotations


class SAVIFile(PadFile):
    """A simple base class that defines basic properties of File object for the use in PAD experiments"""

    def __init__(self, client_id, path, attack_type=None, file_id=None):
        """**Constructor Documentation**

        Initialize the Voice File object that can read WAV files.

        Parameters:

        For client_id, path, attack_type, and file_id, please refer
        to :py:class:`bob.pad.base.database.PadFile` constructor
        """

        super(SAVIFile, self).__init__(client_id, path, attack_type, file_id)

        if self.is_tampered():
            self.attack_type = 'tampered'

    def load(self, directory=None, extension='.wav'):
        path = self.make_path(directory, extension)
        if extension == '.wav':
            if self.is_video_tampered():
                # determine the original audio name and load that instead
                path = self.path_non_tampered_version(directory, extension)
            # check for empty files
            if not os.path.exists(path) or os.stat(path).st_size == 0:
                return 0, numpy.array([])
            rate, audio = scipy.io.wavfile.read(path)
            # We consider there is only 1 channel in the audio file => data[0]
            return rate, numpy.cast['float'](audio)
        elif extension == '.avi' or extension == '.mp4':
            if self.is_audio_tampered():
                # determine the original video name and load that instead
                path = self.path_non_tampered_version(directory, extension)
            # check for empty files
            if os.stat(path).st_size == 0:
                return 0
            videoreader = bob.io.video.reader(path)
            # just return a number of frames to not occupy a memory in case of large videos
            # return videoreader.number_of_frames
            # return videoreader.load()
            return videoreader  # the readers allows to read video frame by frame

    def is_video_tampered(self):
        # tampered videos have '-video-' in their names
        return '-video-' in self.make_path()

    def is_audio_tampered(self):
        # tampered audios have '-audio-' in their names
        return '-audio-' in self.make_path()

    def is_tampered(self):
        # tampered videos have '-audio-' in their names
        return (self.is_audio_tampered() or self.is_video_tampered())

    def path_non_tampered_version(self, directory=None, extension=''):
        if self.is_audio_tampered():
            non_tampered_path = self.make_path(directory).split('-audio-')[0] + extension
        elif self.is_video_tampered():
            non_tampered_path = self.make_path(directory).split('-video-')[0] + extension
        else:
            non_tampered_path = self.make_path(directory, extension)
        # if this path does not exist, try find it in the directory
        # where original non tampered versions are located.
        # if "_tampered" in non_tampered_path:
        # import ipdb; ipdb.set_trace()
        if not os.path.exists(non_tampered_path):
            non_tampered_path = non_tampered_path.replace("_tampered", "_nontampered")
        # if still does not exists, use the same path as the tampered one
        # if not os.path.exists(non_tampered_path):
        #     return self.make_path(directory, extension)
        return non_tampered_path


class SAVIPadDatabase(FileListPadDatabase):
    def __init__(self,
                 original_directory="[SAVI_DATA_DIRECTORY]",
                 original_extension=".wav",
                 db_name='',
                 pad_file_class=SAVIFile,
                 **kwargs):
        # call base class constructor
        if not os.path.isdir(db_name):
            from pkg_resources import resource_filename
            folder = resource_filename(__name__, '../lists/' + db_name)
        else:
            # if a db_name is in fact a directory, this means it's our folder
            # and the name of the last folder is db_name
            folder = db_name
            db_name = os.path.split(db_name)[-1]

        super(SAVIPadDatabase, self).__init__(folder, db_name, pad_file_class=pad_file_class,
                                              original_directory=original_directory,
                                              original_extension=original_extension,
                                              **kwargs)                                     

    def annotations(self, annotation_file):
        # FrameContainer used by bob.bio.video expect frame indexes to be
        # strings
        # print 'Inside SAVIPadDatabase - annotations \n', annotation_file, '\n' 
        annotations = _annotations(self.original_directory, annotation_file)
        annotations = {str(key): annotations[key] for key in annotations}
        return annotations

    def tobjects(self, groups=None, protocol=None, model_ids=None, **kwargs):
        pass

    def zobjects(self, groups=None, protocol=None, **kwargs):
        pass

    def model_ids_with_protocol(self, groups=None, protocol=None, **kwargs):
        return []

    def tmodel_ids_with_protocol(self, protocol=None, groups=None, **kwargs):
        return []

# class SAVIPadDatabaseFaceNet( FileListPadDatabase ):
#     def __init__(self,
#                  original_directory="[SAVI_DATA_DIRECTORY]",
#                  original_extension=".wav",
#                  db_name='',
#                  pad_file_class=SAVIFile,
#                  **kwargs):
#         # call base class constructor
#         from pkg_resources import resource_filename
#         folder = resource_filename(__name__, '../lists/' + db_name)
#         super(SAVIPadDatabase, self).__init__(folder, db_name, pad_file_class=pad_file_class,
#                                               original_directory=original_directory,
#                                               original_extension=original_extension,
#                                               **kwargs)
# 
#     def annotations( self, annotation_file ):
#         print( "Nothing in here\n" )
# 
#     def tobjects(self, groups=None, protocol=None, model_ids=None, **kwargs):
#         pass
# 
#     def zobjects(self, groups=None, protocol=None, **kwargs):
#         pass
# 
#     def model_ids_with_protocol(self, groups=None, protocol=None, **kwargs):
#         return []
# 
#     def tmodel_ids_with_protocol(self, protocol=None, groups=None, **kwargs):
#         return []

class SAVIBioDatabase(SAVIPadDatabase):
    """
    Implements verification API for querying SAVI database.
    """

    def __init__(self,
                 original_directory="[SAVI_DATA_DIRECTORY]",
                 original_extension=".wav",
                 db_name='',
                 **kwargs):
        # call base class constructors to open a session to the database
        super(SAVIBioDatabase, self).__init__(name=db_name,
                                              original_directory=original_directory,
                                              original_extension=original_extension, **kwargs)

        self.low_level_group_names = ('train', 'dev', 'eval')
        self.high_level_group_names = ('world', 'dev', 'eval')

    def model_ids_with_protocol(self, groups=None, protocol=None, **kwargs):
        groups = self.convert_names_to_lowlevel(groups, self.low_level_group_names, self.high_level_group_names)
        return [client.id for client in self.clients(groups=groups, **kwargs)]

    def objects(self, protocol=None, purposes=None, model_ids=None, groups=None, **kwargs):

        # convert group names from the conventional names in verification experiments to the internal database names
        if groups is None:  # all groups are assumed
            groups = self.high_level_group_names
        matched_groups = self.convert_names_to_lowlevel(groups, self.low_level_group_names, self.high_level_group_names)

        # this conversion of the protocol with appended '-licit' or '-spoof' is a hack for verification experiments.
        # To adapt spoofing databases to the verification experiments, we need to be able to split a given protocol
        # into two parts: when data for licit (only real/genuine data is used) and data for spoof (attacks are used instead
        # of real data) is used in the experiment. Hence, we use this trick with appending '-licit' or '-spoof' to the
        # protocol name, so we can distinguish these two scenarios.
        # By default, if nothing is appended, we assume licit protocol.
        # The distinction between licit and spoof is expressed via purposes parameters, but
        # the difference is the terminology only.

        # lets check if we have an appendix to the protocol name
        appendix = None
        if protocol:
            appendix = protocol.split('-')[-1]

        # if protocol was empty or there was no correct appendix, we just assume the 'licit' option
        if not (appendix == 'licit' or appendix == 'spoof'):
            appendix = 'licit'
        else:
            # put back everything except the appendix into the protocol
            protocol = '-'.join(protocol.split('-')[:-1])

        # if protocol was empty, we set it to the None
        if not protocol:
            protocol = None

        # licit protocol is for real access data only
        if appendix == 'licit':
            # by default we assume all real data, since this database has no enroll data
            if purposes is None:
                purposes = ('real',)
            elif 'probe' in purposes:
                purposes.remove('probe')
                purposes.append('real')

        # spoof protocol uses real data for enrollment and spoofed data for probe
        # so, probe set is the same as attack set
        if appendix == 'spoof':
            # we return attack data only, since this database does not have enroll
            if purposes is None:
                purposes = ('attack',)
            # otherwise replace 'probe' with 'attack'
            elif 'probe' in purposes:
                purposes.remove('probe')
                purposes.append('attack')

        # now, query the actual SAVI database
        objects = super(SAVIBioDatabase, self).objects(protocol=protocol, groups=matched_groups,
                                                       purposes=purposes, **kwargs)
        # make sure to return BioFile representation of a file, not the database one
        return [SAVIFile(f.client_id, f.path, file_id=f.file_id) for f in objects]


class SAVIBioFile(SAVIFile):
    def __init__(self, client_id, path, attack_type=None, file_id=None):
        """**Constructor Documentation**

        Initialize the File object that can load video and audio files.

        Parameters:

        For client_id, path, attack_type, and file_id, please refer
        to :py:class:`bob.pad.base.database.PadFile` constructor
        """

        super(SAVIBioFile, self).__init__(client_id, path, attack_type, file_id)

    def load(self, directory=None, extension='.avi', frame_selector=None):
        path = self.make_path(directory, extension)
        # import ipdb; ipdb.set_trace()
        if extension == '.avi'  or extension == '.mp4':
            if self.is_audio_tampered():
                # determine the original video name and load that instead
                path = self.path_non_tampered_version(directory, extension)
            # check for empty files
            if os.stat(path).st_size == 0:
                return None
            # video = bob.io.video.reader(path)
            # just return a number of frames to not occupy a memory in case of large videos
            # vid = video.load()
            # return vid[10]
            if frame_selector:
                return frame_selector(path, load_function=bob.io.video.reader)
            return bob.io.video.reader(path)


class SAVIProperBioDatabase(HighBioDatabase):
    """
    Implements verification API for querying SAVI database.
    """

    def __init__(self,
                 original_directory="[SAVI_DATA_DIRECTORY]",
                 original_extension=".wav",
                 db_name='',
                 **kwargs):

        from pkg_resources import resource_filename
        folder = resource_filename(__name__, '../lists/' + db_name)
        # call base class constructors to open a session to the database
        super(SAVIProperBioDatabase, self).__init__(filelists_directory=folder,
                                                    db_name=db_name, file_class=SAVIBioFile,
                                                    original_directory=original_directory,
                                                    original_extension=original_extension,
                                                    **kwargs)

    def model_ids_with_protocol(self, groups=None, protocol=None, **kwargs):
        """
        We call the BioFileList parent of the database, which understands 'for_model.lst' file 
        and can return model_ids from there.
        """
        # make sure we convert the group names from PAD to BIO convention
        groups = self.convert_names_to_lowlevel(groups, self.low_level_group_names, self.high_level_group_names)
        # make sure we convert the protocol name, since it can have '-licit' or '-spoof' appendix
        return super(HighBioDatabase, self).client_ids(protocol=self._convert_protocol(protocol)[0], groups=groups, **kwargs)

    def _convert_purposes(self, purposes, modifier):
        """
        We assume that in addition to PAD file lists, there are two additional file lists
        from verification database: for_model.lst and for_probe.lst files that specify
        enrollment and probe data.

        Args:
            purposes: The original purposes supplied by Bio verification framework
            modifier: Indicates whether it is licit or spoof scenario

        Returns: corrected purposes according to either licit or spoof scenarios

        """

        if isinstance(purposes, str):
            purposes = [purposes]
        elif purposes is not None:
            purposes = list(purposes)

        # for licit scenario we do not change purposes,
        # since they would be coming from the Bio interface
        # and out DB has these lists
        if purposes is None:
            purposes = ['enroll', 'probe']

        # spoof scenario uses spoofed data for probe
        # but, during scoring, this scenario also needs a real-probe data
        # for cases when model_id is equal to client_id
        # Hence, we request both real and attack data
        if modifier == 'spoof':
            # we return enroll, probe, and attack data
            if 'probe' in purposes:
                purposes.append('attack')

        return purposes

    def annotations(self, annotation_file):
        # FrameContainer used by bob.bio.video expect frame indexes to be
        # strings
        annotations = _annotations(self.original_directory, annotation_file)
        annotations = {str(key): annotations[key] for key in annotations}
        return annotations

    def objects(self, groups=None, protocol=None, purposes=None, model_ids=None, **kwargs):
        # convert group names from the conventional names in verification experiments to the internal database names
        if groups is None:  # all groups are assumed
            groups = self.high_level_group_names
        matched_groups = self.convert_names_to_lowlevel(groups, self.low_level_group_names, self.high_level_group_names)

        protocol, modifier = self._convert_protocol(protocol)
        purposes = self._convert_purposes(purposes, modifier)

        # first check if we have attacks and,
        # for them, query the PAD version of the database
        attack_objects = None
        if 'attack' in purposes:
            attack_objects = self._pad_db.objects(protocol=protocol, groups=matched_groups,
                                                  purposes=('attack',), **kwargs)
            purposes.remove('attack')

        # for real data, we assume there are for_models.lst and for_probe.lst file lists
        # of the verification Filielist database,
        # so we query this Bio version of the database
        # notice we use original 'groups' and also model_ids
        objects = []
        if purposes:
            objects = super(HighBioDatabase, self).objects(groups=groups, protocol=protocol,
                                                           purposes=purposes, model_ids=model_ids, **kwargs)

        if attack_objects:
            objects += attack_objects

        # note that PAD database does not know anything about model_ids, so these are ignored
        # Hence, for the spoofing protocol, we need to filter out the files and
        # keep only those that belong to model_ids
        # We also modify the client_id to reflect that it is an attack
        if modifier == 'spoof' and model_ids is not None:
            objects = self._filter_by_model_ids(objects, model_ids)

        # all objects are of SAVIBioFile class, since this is the class we used in __init__()
        return objects
