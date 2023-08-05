#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Wed 23 Aug 11:12:22 CEST 2017
#


"""
The script generates a set of non-tampered videos from a given database for SAVI-MediFor project.
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
                        help="The root directory of a given database video data.")

    parser.add_argument('-o', '--output-directory', required=False, type=str, default="train",
                        help="The output directory, where all files are written to.")

    parser.add_argument('-s', '--skip-keywords', required=False, nargs='+', default=["head"],
                        help="Names of the folders inside root dir that will be skipped during processing.")

    # parse arguments
    args = parser.parse_args(command_line_parameters)

    return args


def main(command_line_parameters=None):
    """Traverses the folder structure of a given database and generate non-tampered video/audio files."""

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
        # these are directories, so ignore files
        if os.path.isfile(speaker_path):
            continue
        # now, go through the video sequences of the speaker
        for video_dir in os.listdir(speaker_path):

            # exclude the silent videos (not corresponding audio for these)
            # for instance, in VidTIMIT see http://conradsanderson.id.au/database/ for details
            do_skip = False
            for skip_word in args.skip_keywords:
                if skip_word in video_dir:
                    do_skip = True
            if do_skip: continue

            video_path = os.path.join(speaker_path, video_dir)
            # these are directories, so ignore files
            if os.path.isfile(video_path):
                continue

            input_images = video_path
            output_video = os.path.join(args.output_directory, speaker_id, video_dir + '.avi')
            # convert images inside each folder into MJPEG videos
            command = "ffmpeg -start_number 1 -framerate 25 -f image2 -i " + input_images + "/%03d -codec copy -an -y " + output_video
            print(command)
            bob.io.base.create_directories_safe(os.path.dirname(output_video))
            subprocess.call(command, shell=True)


if __name__ == '__main__':
    main()
