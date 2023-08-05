# coding=utf-8


"""

Extract audio features from supplied video files and save the results in <pwd> with the same image/video name.

"""

from __future__ import print_function

import os
import sys
import math
import argparse

# import bob.io.video

import subprocess

# import bob.core
# logger = bob.core.log.setup("bob.paper.lipsync2019")


def command_line_arguments(command_line_parameters):
    """Defines the command line parameters that are accepted."""

    parser = argparse.ArgumentParser(description=__doc__, conflict_handler='resolve',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-l', '--list-files', required=False, default=None,
                        help="The list of video files, from which we extract audio.")

    parser.add_argument('-p', '--prefix-directory', required=False, default="",
                        help="The prefix path that will be appended either to database-directory or paths of video "
                             "files in the files list.")

    parser.add_argument('-d', '--database-directory', required=False, default=None,
                        help="The directory with video data, from which we extract audio.")

    parser.add_argument('-o', '--output-directory', required=False, default="temp",
                        help="The directory, where extracted audio will be stored.")

    # # add verbose option
    # bob.core.log.add_command_line_option(parser)

    # parse arguments
    args = parser.parse_args(command_line_parameters)

    # set verbosity level
    # bob.core.log.set_verbosity_level(logger, args.verbose)

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


def extract_audio(inpath, outpath):
    """

    """
    inpath = inpath.strip()
    outpath = outpath.strip()
    outpath = os.path.splitext(outpath)[0] + '.wav'
    if inpath.endswith(".mp4") or inpath.endswith(".avi"):
        print (inpath, outpath)
        # use ffmpeg to extract audio (one channel of 16K freq audio) from video files
        command = "ffmpeg -i " + inpath + " -ac 1 -ar 16000 -vn -y " + outpath
        subprocess.call(command, shell=True)


def process_file_list(list_files, outdirectory, prefix_directory=""):
    with open(list_files) as f:
        inlines = f.readlines()

        for video_path in inlines:
            video_path = video_path.strip()
            # find the name of the video and add the extension
            video_name = os.path.basename(video_path)
            # if the video name is given as a relative path, we want to recreated the same path structure for output
            video_subdir = os.path.dirname(video_path)
            video_dir = os.path.join(outdirectory, video_subdir)
            create_directories_safe(video_dir)
            # create an output path
            outpath = os.path.join(video_dir, video_name)
            extract_audio(os.path.join(prefix_directory, video_path) + ".mp4", outpath)


def process_directory(indirectory, outdirectory, prefix_directory=""):
    """

    Args:
        indirectory: Where the video data is
        outdirectory: Where the audio files (with preserved relative paths) should be
        prefix_directory: The base directory starting from which, the relative folder structure should be preserved

    Returns:
        Command line example: bin/extract_audio_from_video.py -d /Volumes/idiap/savi/data/idiapset -o
        /Volumes/idiap/savi/data/idiapset -p /Volumes/idiap/savi/data/idiapset/

    """
    for root, dirs, files in os.walk(indirectory):
        # go through files in the subdirectories
        for video_name in files:
            # print(root, dirs, files)
            video_path = os.path.join(root, video_name)
            # if the indirectory is a relative path, we want to recreated the same path structure for output
            # video_subdir = video_path.split(prefix_directory)[0]
            # video_dir = os.path.join(outdirectory, video_subdir)
            # create_directories_safe(video_dir)

            # construct the output path
            # take the right relative path from input by removing prefix_directory
            video_relative_path = video_path.split(prefix_directory)[1]
            # create_directories_safe(video_relative_path)
            # append relative path to the output directory
            outpath = os.path.join(outdirectory, video_relative_path)
            # make sure dir for the output video exists
            create_directories_safe(os.path.dirname(outpath))
            extract_audio(video_path, outpath)


def main(command_line_parameters=None):

    # Collect command line arguments
    opts = command_line_arguments(command_line_parameters)

    # Create output directory
    create_directories_safe(opts.output_directory)

    # Process input files
    if opts.list_files:
        process_file_list(opts.list_files, opts.output_directory, opts.prefix_directory)
    elif opts.database_directory:
        process_directory(opts.database_directory, opts.output_directory, opts.prefix_directory)
    else:
        raise ValueError("Please provide either a text file with the list of video files or a path to folder with "
                         "video files")


if __name__ == '__main__':
    main()
