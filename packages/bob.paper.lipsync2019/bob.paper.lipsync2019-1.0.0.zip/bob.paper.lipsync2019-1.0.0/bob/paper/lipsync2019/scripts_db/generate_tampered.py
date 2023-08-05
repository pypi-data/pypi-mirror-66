#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>

"""
The script generates tampered video/audio pairs for GRID Corpus database by randomly mapping video to different
audio. This is for SAVI project.

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
import pickle

#import bob.io.base

def command_line_arguments(command_line_parameters):
    """Parse the program options"""

    epilog = "Example of running this command:\n\n" \
             "\tpython generate_tampered.py -d /Volumes/data -o /out/dir/vidtimit_tampered -t 5"
    # set up command line parser
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     epilog=epilog)

    parser.add_argument('-d', '--database-directory', required=False, default=".",
                        help="The root directory of database data.")

    parser.add_argument('-o', '--output-directory', required=False, default=".",
                        help="The directory where to store tampered videos.")

    parser.add_argument('-t', '--number-of-tampered', required=False, default=1,
                        help="How many different audio tracks for each video, i.e., defines number of tampered "
                             "videos for each original video.")

    parser.add_argument('-s', '--seed', required=False, default=1,
                        help="Set the seed of the random generator.")

    # parse arguments
    args = parser.parse_args(command_line_parameters)

    return args


def files_4each_speaker(rootdir):
    speakers_files = {}
    # go through each speaker (directory) of the database
    for speaker_id in os.listdir(rootdir):
        speaker_path = os.path.join(rootdir, speaker_id)
        if os.path.isfile(speaker_path):
            continue

        for root, dirs, files in os.walk(speaker_path):
            for f in files:
                if not f.endswith(".avi"): continue
                orig_video_path = os.path.join(root, f)
                if speaker_id not in speakers_files:
                    speakers_files[speaker_id] = []
                # remove extension
                orig_video_path, _ = os.path.splitext(orig_video_path)
                speakers_files[speaker_id].append(orig_video_path)

    return speakers_files


def main(command_line_parameters=None):

    # Set the directory you want to start from
    args = command_line_arguments(command_line_parameters)

    # set the seed of the random generator
    numpy.random.seed(int(args.seed))

    rootdir = os.path.curdir
    if args.database_directory:
        rootdir = args.database_directory
    if not rootdir.endswith('/'):
        rootdir += '/'
    number_of_tampered = int(args.number_of_tampered)

    # create the output directory if it does not exist
    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)

    pickled_file = 'speakers_files.pkl'
    if os.path.exists(pickled_file):
        with open(pickled_file, 'rb') as f:
            speakers_files = pickle.load(f)
    else:
        speakers_files = files_4each_speaker(rootdir)
        with open('speakers_files' + '.pkl', 'wb') as f:
            pickle.dump(speakers_files, f, pickle.HIGHEST_PROTOCOL)

    speaker_ids = numpy.array(sorted(list(speakers_files.keys())))
    num_speakers = len(speaker_ids)

    for tampering_pass in range(number_of_tampered):
        for correct_speaker in speaker_ids:
            correct_speaker_files = speakers_files[correct_speaker]
            cur_num_files = len(correct_speaker_files)
            # for each of our current speaker video files,
            # we want to find a random audio file(s) from a random speaker to create tampered video
            tampered_indices = numpy.random.permutation(num_speakers)
            # remove current correct_speaker from the tampered candidates
            # first, find the index of the current speaker
            index_speaker = numpy.argwhere(speaker_ids==correct_speaker)
            # remove this index from tampered candidates
            index_tampered = numpy.argwhere(tampered_indices==index_speaker)
#            import ipdb; ipdb.set_trace()
#            print("##index_tampered", index_tampered)
            tampered_indices = numpy.delete(tampered_indices, index_tampered)

            # make sure tampered_indices is long enough for all files of the
            # current correct speaker
            tampered_indices = numpy.tile(tampered_indices, int(cur_num_files/len(tampered_indices)+1))

            # for each video file of the correct speaker
            for i, cur_file in zip(range(cur_num_files), correct_speaker_files):
                # import ipdb; ipdb.set_trace()
                # get all audio files from target speaker
                target_speaker = speaker_ids[tampered_indices[i]]
                target_speaker_files = speakers_files[target_speaker]
                num_target_files = len(target_speaker_files)
                target_files_indices = numpy.arange(num_target_files)
                while len(target_files_indices) < cur_num_files:
                    target_files_indices = numpy.append(target_files_indices, numpy.arange(num_target_files))

                if target_files_indices.shape[0] < cur_num_files:
                    raise ValueError("Speaker {0} and {1}  should have the same number of audio files, but now it's {2} and {3}".format(
                        correct_speaker, target_speaker, cur_num_files, target_files_indices.shape[0]))

                # compute output video and audio files as correct speaker name plus
                # the name of the random speaker we take the audio from
                if rootdir not in cur_file:
                    raise ValueError("Current video file '{0}' is not rooted in this directoty: {1}".format(cur_file, rootdir))
                out_video_name = cur_file.split(rootdir)[1]
                out_audio_name = out_video_name
                out_video_name += "-audio-" + target_speaker + ".avi"
                out_audio_name += "-audio-" + target_speaker + ".wav"
                out_video_name = os.path.join(args.output_directory, out_video_name)
                out_audio_name = os.path.join(args.output_directory, out_audio_name)

                if os.path.exists(out_video_name):
                    continue
                audio_source = target_speaker_files[target_files_indices[i]]
#                audio_source = target_speaker_files[i]
                audio_name = audio_source.split('/')[-1]
                video_name = out_video_name.split('/')[-1][:-4]
                video_name = video_name.split('-audio')[0]
                print("%s:%s %s:%s" % (correct_speaker, video_name, target_speaker, audio_name))
                if not os.path.exists(os.path.dirname(out_video_name)):
                    os.makedirs(os.path.dirname(out_video_name))
                shutil.copyfile(audio_source + '.wav', out_audio_name)


if __name__ == '__main__':
    main()
