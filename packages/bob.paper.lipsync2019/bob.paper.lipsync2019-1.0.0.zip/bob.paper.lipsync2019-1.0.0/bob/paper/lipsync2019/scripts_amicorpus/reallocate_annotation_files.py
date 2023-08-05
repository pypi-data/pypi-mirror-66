# coding=utf-8


"""

Copy features from supplied video files and save the results in <pwd> with the same image/video name.

"""

from __future__ import print_function

import os
from shutil import copyfile
import argparse

# import bob.io.video

import subprocess
import threading

import sys
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue

# import bob.core
# logger = bob.core.log.setup("bob.paper.lipsync2019")


def command_line_arguments(command_line_parameters):
    """Defines the command line parameters that are accepted."""

    parser = argparse.ArgumentParser(description=__doc__, conflict_handler='resolve',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-a', '--annotation-directory', required=False, default=None,
                        help="The directory with hdf5 files, from which we copy them.")

    parser.add_argument('-o', '--output-directory', required=False, default="temp",
                        help="The directory, where annotation hdf5 file should be copied.")

    # add verbose option
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


def copy_subprocess(cmd):
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def copy_system_command(cmd):
    os.system(cmd)
    # proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE


filename_queue = queue.Queue()


def thread_copier():
    while True:
        filenames = filename_queue.get()
        if filenames is None:  # EOF?
            return
        # subpr = copy_subprocess(['rsync --size-only --no-R --no-implied-dirs ', filenames[0], filenames[1]])
        # subpr.wait()
        print("copied %s to %s" % (filenames[0], filenames[1]))


def process_directory(indirectory, outdirectory, prefix_directory=""):
    """

    Args:
        indirectory: Where the hdf5 files to copy are
        outdirectory: Where the video files for which we want to copy hdf5 file are
        prefix_directory: The base directory starting from which, the relative folder structure should be preserved

    Returns:
        Command line example: bin/rellocate_annotation_files.py -a /Volumes/idiap/savi/features/preprocessed/idiapset -o
        /Volumes/idiap/savi/features/idiaptampered

    """

    for root, dirs, files in os.walk(indirectory):
        # go through files in the subdirectories
        for file_name in files:
            if not file_name.endswith('av.hdf5'): continue
            # print(root, dirs, files)
            hdf5_path = os.path.join(root, file_name)
            # remove extension
            hdf5_without_extension, _ = os.path.splitext(file_name)
            # remove prefix directory
            hdf5_relative_path = os.path.relpath(hdf5_path, indirectory)
            # remove the file name
            hdf5_relative_stem = os.path.dirname(hdf5_relative_path)
            output_hdf5_dir = os.path.join(outdirectory, hdf5_relative_stem)
            if not os.path.isdir(output_hdf5_dir):
                create_directories_safe(output_hdf5_dir)

            for avifile in os.listdir(output_hdf5_dir):
                if hdf5_without_extension in avifile and avifile.endswith('audio.hdf5'):
                    output_without_extension = avifile.split('-audio.hdf5')[0]
                    outpath = os.path.join(output_hdf5_dir, output_without_extension + ".hdf5")
                    # if exists, skip it
                    if os.path.isfile(outpath):
                        print("Skipping existing %s" % outpath)
                        continue
                    print (hdf5_path, outpath)
                    # filename_queue.put((hdf5_path, outpath))
                    copy_system_command('rsync --size-only --no-R --no-implied-dirs %s %s' % (hdf5_path, outpath))
                    # copy_system_command('cp %s %s' % (hdf5_path, outpath))
                    # copyfile(hdf5_path, outpath)

    # threads = [threading.Thread(target=thread_copier) for _i in range(10)]
    # for thread in threads:
    #     thread.start()
    #     filename_queue.put(None)  # one EOF marker for each thread

def main(command_line_parameters=None):

    # Collect command line arguments
    opts = command_line_arguments(command_line_parameters)

    # Create output directory
    create_directories_safe(opts.output_directory)

    process_directory(opts.annotation_directory, opts.output_directory)


if __name__ == '__main__':
    main()
