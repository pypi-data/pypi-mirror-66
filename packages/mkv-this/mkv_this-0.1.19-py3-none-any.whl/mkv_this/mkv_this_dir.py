#! /usr/bin/env python3

"""
    mkv-this-dir: input a directory, output markovified text based on all its text files.
    Copyright (C) 2020 mousebot@riseup.net.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

"""
a (very basic) script to collect all text files in a directory, markovify them and output a user-specified number of sentences to a text file.
"""
     
import markovify
import sys
import argparse
import os

def main():
    
    # argparse for cmd line args
    parser = argparse.ArgumentParser()

    # positional args:
    parser.add_argument('indir', help="the directory to extract the text of all text files from, with path.")
    parser.add_argument('outfile', nargs='?', default="./mkv-dir-output.txt", help="the file to save to, with path. if the file is used more than once, subsequent literature will be appended to the file after a star. defaults to ./mkv-dir-output.txt.")

    # optional args:
    parser.add_argument('-s', '--statesize', help="the number of preceeding words the probability of the next word depends on. defaults to 2, 1 makes it more random, 3 less so.", type=int, default=2)
    parser.add_argument('-n', '--sentences', help="the number of 'sentences' to output. defaults to 5.", type=int, default=5)
    parser.add_argument('-l', '--length', help="set maximum number of characters per sentence.", type=int)
    parser.add_argument('-o', '--overlap', help="the amount of overlap allowed between original text and the output, expressed as a radio between 0 and 1. lower values make it more random. defaults to 0.5", type=float, default=0.5)
    parser.add_argument('-c', '--combine', help="provide an another input text file with path to be combined with the first.")
    parser.add_argument('-w', '--weight', help="specify the weight to be given to the second text provided with --combine. defaults to 1, and the weight of the initial text is also 1. setting this to 1.5 will place 50 percent more weight on the second text. setting it to 0.5 will place less.", type=float, default=1)

    args = parser.parse_args()

    #create a list of files to concatenate:
    matches = []
    for root, dirnames, filenames in os.walk(args.indir):
        for filename in filenames:
            if filename.endswith(('.txt', '.org', '.md')):
                matches.append(os.path.join(root, filename))

    # concatenate the files into batchfile.txt:
    batchfile = os.path.dirname(args.indir) + os.path.sep + 'batchfile.txt' # SEEMS like it works?

    with open(batchfile, 'w') as outfile:    
        for fname in matches:
            with open(fname) as infile:
                outfile.write(infile.read())

    # Get raw text from batchfile as string.
    with open(batchfile, 'r') as f:
        text = f.read()
    
    # Build the model:
    # NB: this errors if infile is EMPTY:
    text_model = markovify.Text(text, state_size=args.statesize)

    # Print -n number of randomly-generated sentences
    for i in range(args.sentences):
        output = open(args.outfile, 'a')  # append to file
        if args.length :
            output.write(str(text_model.make_short_sentence(
                args.length, tries=500, max_overlap_ratio=args.overlap)) + '\n \n')
        else:
            output.write(str(text_model.make_sentence(
                tries=500, max_overlap_ratio=args.overlap)) + '\n \n')
            # \n to add newline between each sentence.
            output.write(str(' \n \n * \n \n'))
            # add a star between each appended set.
        output.close()

    os.unlink(batchfile)

    print('\n:  literary genius has been written to the file ' + args.outfile + '. thanks for playing!')
    sys.exit()
