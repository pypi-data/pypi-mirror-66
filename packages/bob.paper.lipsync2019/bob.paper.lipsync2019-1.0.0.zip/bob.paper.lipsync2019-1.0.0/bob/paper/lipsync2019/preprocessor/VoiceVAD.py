#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""
This preprocessor reads audio files and computes 2GMM-based VAD.
The results are saved to files in format: <name>'-audio'.ext.
"""

import bob.ip.base
import bob.ip.color
import os

from bob.bio.spear.preprocessor import Energy_2Gauss

import bob.core
logger = bob.core.log.setup("bob.paper.lipsync2019")


class VoiceVAD(Energy_2Gauss):
    """
    Computes optical flow on video frames.

    """

    def __init__(
            self,
            **kwargs
    ):
        Energy_2Gauss.__init__(self, **kwargs)

    def write_data(self, data, data_file, compression=0):
        hdf5_path, ext = os.path.splitext(data_file)
        hdf5_path += '-audio' + ext
        f = bob.io.base.HDF5File(hdf5_path, 'w')
        f.set("rate", data[0], compression=compression)
        f.set("data", data[1], compression=compression)
        f.set("labels", data[2], compression=compression)

    def read_data(self, data_file):
        hdf5_path, ext = os.path.splitext(data_file)
        hdf5_audio_path = hdf5_path + '-audio' + ext
        f = bob.io.base.HDF5File(hdf5_audio_path)
        rate = f.read("rate")
        data = f.read("data")
        labels = f.read("labels")
        return rate, data, labels

    def __call__(self, frames, annotations=None):
        """__call__(frames, annotations = None) -> face

        """
        if frames[0] == 0:  # the file was empty or did not exist
            return None
        return Energy_2Gauss.__call__(self, frames, annotations)
