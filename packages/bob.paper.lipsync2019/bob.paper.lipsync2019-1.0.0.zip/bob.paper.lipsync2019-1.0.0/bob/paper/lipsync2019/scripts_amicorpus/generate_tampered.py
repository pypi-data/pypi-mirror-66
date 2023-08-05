#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>

"""
The script generates text file lists for protocols of the SAVI data.

"""
from __future__ import print_function

import os
import math
import argparse
import numpy
import shutil
import csv
import re
import subprocess

# import bob.io.base

def command_line_arguments(command_line_parameters):
    """Parse the program options"""

    epilog = "Example of running this command:\n\n" \
             "\tpython generate_tampered.py -d /Volumes/data -t 10"
    # set up command line parser
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     epilog=epilog)

    parser.add_argument('-d', '--database-directory', required=False, default=".",
                        help="The root directory of database data.")

    parser.add_argument('-a', '--annotation-directory', required=False, default=".",
                        help="The root directory with annotation files.")

    parser.add_argument('-o', '--output-directory', required=False, default=".",
                        help="The directory where to store tampered videos.")

    parser.add_argument('-t', '--number-of-tampered', required=False, default=1,
                        help="How many different audio tracks for each video, i.e., defines number of tampered "
                             "videos for each original video.")

    # parse arguments
    args = parser.parse_args(command_line_parameters)

    return args


def create_directories_safe(directory, dryrun=False):
  """Creates a directory if it does not exists, with concurrent access support.
  This function will also create any parent directories that might be required.
  If the dryrun option is selected, it does not actually create the directory,
  but just writes the (Linux) command that would have been executed.

  **Parameters:**

  ``directory`` : str
    The directory that you want to create.

  ``dryrun`` : bool
    Only ``print`` the command to console, but do not execute it.
  """
  try:
    if dryrun:
      print("[dry-run] mkdir -p '%s'" % directory)
    else:
      if directory and not os.path.exists(directory):
        os.makedirs(directory)

  except OSError as exc:  # Python >2.5
    import errno
    if exc.errno != errno.EEXIST:
      raise


def files_4each_speaker(rootdir):
    speakers_files = {}
    for root, dirs, files in os.walk(rootdir):
        for f in files:
            if not f.endswith(".avi"): continue
            orig_video_path = os.path.join(root, f)
            file_name = os.path.basename(f)
            speaker_id = file_name.split('-')[0]
            if speaker_id not in speakers_files:
                speakers_files[speaker_id] = []
            # remove extension
            orig_video_path, _ = os.path.splitext(orig_video_path)
            speakers_files[speaker_id].append(orig_video_path)

    return speakers_files


def main(command_line_parameters=None):
    # Set the directory you want to start from
    args = command_line_arguments(command_line_parameters)

    rootdir = os.path.curdir
    if args.database_directory:
        rootdir = args.database_directory

    annotdir = args.annotation_directory
    number_of_tampered = int(args.number_of_tampered)

    # create the output directory if it does not exist
    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)

    speakers_files = files_4each_speaker(rootdir)
    speaker_ids = numpy.array(speakers_files.keys())
    num_speakers = len(speaker_ids)

    for tampering_pass in range(number_of_tampered):
        for correct_speaker in speaker_ids:
            correct_speaker_files = speakers_files[correct_speaker]
            cur_num_files = len(correct_speaker_files)
            tampered_indices = numpy.random.permutation(num_speakers)
            # for each of our current speaker video files,
            # we want to find a random audio file(s) from a random speaker to create tampered video
            while correct_speaker in tampered_indices[:cur_num_files]:
                tampered_indices = numpy.random.permutation(num_speakers)

            # remove all target speakers with small number of files
            for index in tampered_indices:
                if len(speakers_files[speaker_ids[index]]) < 4:
                    tampered_indices = numpy.delete(tampered_indices, numpy.where(tampered_indices==index))

            # make sure tampered_indices is long enough
            for i in range(int(cur_num_files/len(tampered_indices))):
                tampered_indices = numpy.append(tampered_indices, tampered_indices)

            print("current speaker: ", correct_speaker)
            # for each video file of the correct speaker
            for i, cur_file in zip(range(cur_num_files), correct_speaker_files):
                # get all audio files from target speaker
                print(i, num_speakers)
                target_speaker = speaker_ids[tampered_indices[i]]
                target_speaker_files = speakers_files[target_speaker]
                # print(target_speaker_files)
                num_target_files = len(target_speaker_files)

                if num_target_files < 2:
                    raise ValueError("This speaker has only one file %s" % str(target_speaker_files))

                target_speaker_files = numpy.random.permutation(target_speaker_files)
                # compute output video as correct video name and tampered audio name
                out_video_name = cur_file.split(rootdir)[1]
                out_video_name += "-audio-" + target_speaker + ".avi"
                out_video_name = os.path.join(args.output_directory, out_video_name)
                command = "ffmpeg -i " + cur_file + ".avi -i " + target_speaker_files[0] + \
                          ".wav -map 0:0 -map 1:0 -c:v copy -c:a copy -shortest -y " + out_video_name
                # command = "ffmpeg -i " + cur_file + ".avi -i " + ".wav -i ".join(target_speaker_files) + \
                #           ".wav -map " + ":0 -map ".join(map(str, range(num_target_files))) + \
                #           ":0 -c:v copy -c:a copy -shortest -y " + out_video_name

                print (command)
                create_directories_safe(os.path.dirname(out_video_name))
                subprocess.call(command, shell=True)

            # print(correct_speaker, tampered_speaker)

if __name__ == '__main__':
    main()
