#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Wed 23 Aug 11:12:22 CEST 2017
#


"""
The script generates a set of non-tampered audio from a given database of SAVI-MediFor project.
"""

from __future__ import print_function

import os
import argparse
import subprocess
import bob.io.base


def command_line_arguments(command_line_parameters):
    """Parse the program options"""

    # set up command line parser
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-d', '--database-directory', required=True, default=".",
                        help="The root directory of the database audio data.")

    parser.add_argument('-o', '--output-directory', required=False, type=str, default="train",
                        help="The output directory, where all files are written to.")

    # parse arguments
    args = parser.parse_args(command_line_parameters)

    return args


def main(command_line_parameters=None):
    """Traverses the folder structure of a given database and generate non-tampered audio files."""

    args = command_line_arguments(command_line_parameters)

    rootdir = os.path.curdir
    if args.database_directory:
        rootdir = args.database_directory

    # create the output directory if it does not exist
    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)

    # go through each speaker (directory) of the database
    for speaker_id in os.listdir(rootdir):
        speaker_path = os.path.join(rootdir, speaker_id)
        if os.path.isfile(speaker_path):
            continue
        # now, go through the audio sequences of the speaker
        for audio_file in os.listdir(speaker_path):
            audio_path = os.path.join(speaker_path, audio_file)
            # these are files, so ignore directories
            if not os.path.isfile(audio_path):
                continue
            if not audio_path.endswith(".wav"):
                continue

            inpath = audio_path
            outpath = os.path.join(args.output_directory, speaker_id, audio_file)
            # convert input audio files to 16 KHz 1 channel audio
            command = "ffmpeg -i " + inpath + " -ac 1 -ar 16000 -vn -y " + outpath
            print(command)
            bob.io.base.create_directories_safe(os.path.dirname(outpath))
            subprocess.call(command, shell=True)


if __name__ == '__main__':
    main()
