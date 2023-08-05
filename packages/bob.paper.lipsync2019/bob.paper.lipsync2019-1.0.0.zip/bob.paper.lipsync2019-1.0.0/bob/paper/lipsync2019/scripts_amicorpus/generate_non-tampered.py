#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <pavel.korshunov@idiap.ch>
# Mon  18 Aug 23:12:22 CEST 2015
#
# Copyright (C) 2012-2015 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the ipyplotied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
The script generates a set of non-tampered video and audio files for SAVI-MediFor project using AMI database.
"""
from __future__ import print_function

import os
import argparse
import math
import subprocess


def parse_annotations_file(annotations_file):
    """
    Parse annotations file into the dictionary. For "result[session_name].person_id", 2 lists are given:
         a list of starting speaking times and a list of ending speaking times
    Args:
        annotations_file: path to the file with speech annotations of AMI database

    Returns: dictionary with annotation information

    """

    resulted_dict = {}
    previous_person_id = ''
    with open(annotations_file) as f:
        lines = f.readlines()

    for line in lines:
        line_parts = line.strip().split()
        session_name = line_parts[0].split('.')[0]
        person_id = line_parts[7] + '-' + line_parts[8]
        start_time = float(line_parts[2])
        duration = float(line_parts[3])
        end_time = start_time + duration
        if session_name not in resulted_dict:
            resulted_dict[session_name] = {}
        session_dict = resulted_dict[session_name]
        if person_id not in session_dict:
            session_dict[person_id] = []
        if previous_person_id == person_id and session_dict[person_id]:
            # print(person_id, previous_person_id, session_dict[person_id]["uninterrupted_segment"])
            session_dict[person_id][-1]["duration"] += duration
            session_dict[person_id][-1]["annotations"].append([start_time, end_time])
        else:
            # print(person_id, previous_person_id, session_dict[person_id]["uninterrupted_segment"])
            session_dict[person_id].append({"duration": duration, "annotations": [[start_time, end_time]]})

        previous_person_id = person_id

    return resulted_dict


def extract_media_segments(input_dir, output_dir, session, person_id, segment_duration, id_mapping, annotations_list):
    start_offset = 2.000
    end_offset = 0.00
    person_audio_id = person_id.split('-')[1]
    # in AMI corpus, audio people ids are from 0 to n but for videos, the ids are from 1 to n+1,
    # and video IDs are mapped in totally different ways than audio. This things is messed up.
    # Different sessions have different mapping. I had to go manually into AMI database and find for each session
    # this mapping, hence I use id_mapping list to know which video is mapped to what audio.
    person_video_id = str(id_mapping[int(person_audio_id)])

    out_path = os.path.join(output_dir, session)
    media_offset = annotations_list[0][0]
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    out_segment_duration = segment_duration - start_offset - end_offset
    out_file_name = person_id + '-' + str(out_segment_duration)

    # create correct audio segment of given duration and starting form the start of annotations_list
    orig_audio_path = os.path.join(input_dir, session, 'audio', session + '.Headset-' + person_audio_id + '.wav')
    out_audio_path = os.path.join(out_path, out_file_name + '.wav')
    command = "ffmpeg -ss " + str(media_offset) + " -i " + orig_audio_path + \
              " -ac 1 -ar 16000 -vn -t " + str(segment_duration) + \
              " -ss " + str(start_offset) + " -sseof " + str(end_offset) + " " + \
              out_audio_path
    # print(command)
    # subprocess.call(command, shell=True)

    # create a corresponding video segment
    orig_video_path = os.path.join(input_dir, session, 'video', session + '.Closeup' + person_video_id + '_orig.avi')
    out_video_path = os.path.join(out_path, out_file_name + '.mp4')
    command = "ffmpeg -ss " + str(media_offset) + " -i " + orig_video_path + \
              " -c:v copy -an -t " + str(segment_duration) + \
              " -ss " + str(start_offset) + " -sseof " + str(end_offset) + " " + \
              out_video_path
    # print(command)
    # subprocess.call(command, shell=True)

    # generate video combined with audio, all in one file
    out_audiovideo_path = os.path.join(out_path, out_file_name + '-av.avi')
    command = "ffmpeg -ss " + str(media_offset) + " -t " + str(segment_duration) + " -i " + orig_video_path + \
              " -ss " + str(media_offset) + " -t " + str(segment_duration) + " -i " + orig_audio_path + \
              " -c:v mpeg4 -b:v 3000k -vtag DX50 -acodec pcm_s16le -ac 1 -ar 16000" + \
              " -ss " + str(start_offset) + " -y " + \
              out_audiovideo_path
    print(command)
    subprocess.call(command, shell=True)

    # write corresponding annotations
    out_annotations_path = os.path.join(out_path, out_file_name + '.spk')
    with open(out_annotations_path, 'w') as f:
        for item in annotations_list:
            start_talk = item[0] - media_offset - start_offset
            end_talk = item[1] - media_offset - start_offset
            if start_talk < 0: start_talk = 0
            if end_talk < 0: continue
            if end_talk > out_segment_duration: end_talk = out_segment_duration
            f.write("%s %s %s\n" % (str(start_talk), str(end_talk), person_id))


def command_line_arguments(command_line_parameters):
    """Parse the program options"""

    # set up command line parser
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-d', '--ami-directory', required=True, default=".",
                        help="The root directory of AMI database data.")

    parser.add_argument('-a', '--annotations-file', required=True, default="p1.dev.mdtm",
                        help="The file with annotations per speaker for AMI database.")

    parser.add_argument('-o', '--output-directory', required=False, type=str, default="train",
                        help="The output directory, where all files are written to.")

    # parse arguments
    args = parser.parse_args(command_line_parameters)

    return args

def main(command_line_parameters=None):
    """Traverses the folder structure of AMI database and generate non-tampered video/audio files."""

    args = command_line_arguments(command_line_parameters)

    rootdir = os.path.curdir
    if args.ami_directory:
        rootdir = args.ami_directory

    # create the output directory if it does not exist
    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)

#    original_ami_sessions = ['IS1000a']
    # DO NOT USE these sessions:
    # 'EN2001d', 'EN2001e', 'IS1000c', 'IS1000d', 'ES2002a' - not synchronized audio/video

    # mapping_video_ids=[[1, 2, 3, 4], [1, 4, 2, 3], [4, 2, 3, 1], [2, 1, 4, 3]]

    original_ami_sessions = {'EN2001a': [1, 4, 2, 3], 'EN2001b': [4, 2, 3, 1], 'EN2006b': [4, 2, 3, 1],
                             'ES2005b': [2, 1, 4, 3], 'ES2005c': [2, 1, 4, 3], 'ES2005d': [2, 1, 4, 3],
                             'ES2006a': [2, 1, 4, 3], 'ES2006b': [2, 1, 4, 3], 'ES2006c': [2, 1, 4, 3],
                             'ES2006d': [2, 1, 4, 3], 'ES2007a': [4, 2, 3, 1], 'ES2007b': [4, 2, 3, 1],
                             'ES2007c': [4, 2, 3, 1], 'ES2007d': [4, 2, 3, 1], 'IN1005': [1, 2, 3, 4],
                             'IS1001a': [1, 2, 3, 4], 'IS1001c': [1, 2, 3, 4], 'IS1002c': [1, 2, 3, 4],
                             'IS1002d': [1, 2, 3, 4], 'IS1003a': [1, 2, 3, 4], 'IS1003c': [1, 2, 3, 4]
                             }
                             # 'IN1001': [1, 2, 3, 4], 'IN1002': [1, 2, 3, 4], 'IN1008': [1, 2, 3, 4],
                             # 'IN1007': [1, 2, 3, 4], 'IN1009': [1, 2, 3, 4], 'IN1012': [1, 2, 3, 4],
                             # 'IN1013': [1, 2, 3, 4], 'IN1014': [1, 2, 3, 4], 'IN1016': [1, 2, 3, 4],
                             # 'IS1000a': [1, 2, 3, 4], 'IS1000b': [1, 2, 3, 4], 'IS1001b': [1, 2, 3, 4]}

#    approx_starting_time = 300 # 5 minutes into the video
    approx_segment_length = 30  # seconds of each segment
#    approx_shift = 500 # seconds between segments
    data_structure = parse_annotations_file(args.annotations_file)

    total_num_people = 0
    total_duration = 0
    for session, id_mapping in original_ami_sessions.items():
        cur_session_data = data_structure[session]
        for person_id, person_data in cur_session_data.items():
            use_person = False
            for data_item in person_data:
                segment_duration = (data_item["annotations"][-1][1] - data_item["annotations"][0][0])
                if (segment_duration > approx_segment_length - 15) and \
                        (segment_duration < approx_segment_length + 15) and \
                        math.fabs(data_item["duration"] - segment_duration) < 5:
                    use_person = True
                    total_duration += segment_duration
                    print (person_id, segment_duration)
                    print (person_id, data_item["annotations"])
                    extract_media_segments(rootdir, args.output_directory, session, person_id, segment_duration,
                                           id_mapping, data_item["annotations"])

            if use_person:
                total_num_people += 1
    print("total number of people: ", total_num_people)
    print("total duration", total_duration)
if __name__ == '__main__':
    main()
