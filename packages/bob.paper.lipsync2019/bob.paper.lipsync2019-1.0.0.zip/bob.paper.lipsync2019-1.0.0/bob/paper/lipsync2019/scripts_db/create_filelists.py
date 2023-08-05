"""
This scripts converts file list of genuine or tampered audio files into required format.

Usage:
    {0} [-v...] [options] [--] <filelist>
    {0} -h | --help
    {0} --version

Arguments:
    <filelist>  A glob path to the text files containing lists of files for conversion.

Options:
    -h --help                       Show this screen.
    --version                       Show version.
    -v, --verbose                   Increases the output verbosity level
    -p, --prefix STR                The beginning of the absolute path inside file lists that should be removed.
    -o, --outputdir STR             Directory where to save the converted file lists.
"""


import os
import sys
import glob
from docopt import docopt


def convert_lines(fname, fname_out, PREFIX):
    converted_lines = []
    print("Converting %s" % fname)
    with open(fname) as f:
        lines = f.readlines()
        for line in lines:
            # remove extension
            line, _ = os.path.splitext(line.strip())
            line = line.split(PREFIX)[1]
            split_line = line.split('/')
            speaker_id = split_line[1]
            if 'for_attack' in fname:
                # add client ID and type of the attack to the line
                converted_line = line + ' ' + speaker_id + ' ' + 'tampered'
            else:
                # add client ID to the line
                converted_line = line + ' ' + speaker_id
            converted_lines.append(converted_line)
    os.remove(fname)
    with open(fname_out, 'w') as f:
        for line in converted_lines:
            f.write('%s\n' % line)


def main():
    args = docopt(__doc__.format(sys.argv[0]), version='0.0.1')
    # print(args)

    filelist_glob = args['<filelist>']
    filelists = glob.glob(filelist_glob)
    PREFIX = os.path.join(args['--prefix'], '')  # make sure we have a trailing slash
    output_dir = args['--outputdir']
    for file_path in filelists:
        if 'for_real' in file_path:
            convert_lines(file_path, os.path.join(output_dir, 'for_real.lst'), PREFIX)
        elif 'for_attack' in file_path:
            convert_lines(file_path, os.path.join(output_dir, 'for_attack.lst'), PREFIX)
        else:
            print('Skipping this file: \t%s' % file_path)


if __name__ == '__main__':
    main()
