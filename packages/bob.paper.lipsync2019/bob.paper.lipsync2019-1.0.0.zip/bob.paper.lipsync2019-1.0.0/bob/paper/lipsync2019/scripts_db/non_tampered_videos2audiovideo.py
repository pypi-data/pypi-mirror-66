#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Wed 23 Aug 11:12:22 CEST 2017
#


"""
The script generates a set of non-tampered video/audio files from GRID Corpus database for SAVI-MediFor project.
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

    parser.add_argument('-p', '--prefix-dir', required=False, type=str, default="",
                        help="The prefix directory path that will be injected into the media file path.")

    # parse arguments
    args = parser.parse_args(command_line_parameters)

    return args


def main(command_line_parameters=None):
    """
    Traverses the folder structure of a given database and generate non-tampered video/audio files.
    """

    args = command_line_arguments(command_line_parameters)

    rootdir = os.path.curdir
    if args.database_directory:
        rootdir = args.database_directory

    # create the output directory if it does not exist
    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)

    # go through each speaker (directory) of the database
    for speaker_id in os.listdir(rootdir):
        # For instance, for GRID Corpus, the path to videos of the speaker with speaker ID 's1'
        # is assumed to be the following:
        # database_grid_dir/s1/video/mpg_6000/*.mpg, so we use file prefix to generate the correct path
        # In CUAVE db, speaker id is the file name, so we should take this into
        # account
        print ("speaker id: ", speaker_id)
        speaker_video_path = os.path.join(rootdir, speaker_id)
        if (args.prefix_dir):
            speaker_video_path = os.path.join(speaker_video_path, args.prefix_dir)

        if os.path.isfile(speaker_video_path):  # if ids are part of video files themselves
            if speaker_id.endswith('.mpg') or speaker_id.endswith('.avi'):
                speaker_video_path = rootdir  # all speakers files are inside one folder
                video_files_list = [speaker_id]  # each speaker has one video file
                speaker_id, _ = os.path.splitext(speaker_id)
            else:
                continue
        else:  # if speakers are folders with files inside
            if not os.path.exists(speaker_video_path):
                continue
            video_files_list = os.listdir(speaker_video_path)

        # now, go through the video sequences of the speaker
        for video_file in video_files_list:
            video_path = os.path.join(speaker_video_path, video_file)
            # these are files, so ignore directories
            if not os.path.isfile(video_path):
                continue
#            if not video_path.endswith(".mpg") and \
#                not video_path.endswith(".avi") and \
#                not video_path.endswith(".mp4") and \
#                not video_path.endswith(".mov") and \
#                not video_path.endswith(".mts"):
#                continue
            if not video_path.endswith(".avi"):
                continue
            inpath = video_path
            file_name, _ = os.path.splitext(video_file)
            outpath_audio = os.path.join(args.output_directory, speaker_id, args.prefix_dir, file_name + '.wav')
            # convert input video files to 16 KHz 1 channel audio
            command = "ffmpeg -i " + inpath + " -ac 1 -ar 16000 -vn -y " + outpath_audio
            print(command)

            bob.io.base.create_directories_safe(os.path.dirname(outpath_audio))
            subprocess.call(command, shell=True)

            outpath_video = os.path.join(args.output_directory, speaker_id, args.prefix_dir, file_name + '.avi')
            # convert input video files to 16 KHz 1 channel video
#           command = "ffmpeg -i " + inpath + " -c:v copy -an -y " + outpath_video
            command = "/idiap/temp/wdroz/software/ffmpeg-4.0-64bit-static/ffmpeg -i " + inpath + " -c:v libx264 -preset slow -crf 22 -an -y " + outpath_video
            print(command)
            subprocess.call(command, shell=True)


if __name__ == '__main__':
    main()
