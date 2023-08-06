#! /usr/bin/env python3

import os
import markovify
import sys
import argparse

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


def main():
    
    # argparse for cmd line args
    parser = argparse.ArgumentParser()

    # positional args:
    parser.add_argument('indir', help="the directory to extract the text of all text files from, with path.")
    parser.add_argument('outfile', nargs='?', default="./mkv-dir-output.txt", help="the file to save to, with path. if the file is used more than once, subsequent literature will be appended to the file after a star. defaults to ./mkv-dir-output.txt.")

    # optional args:
    parser.add_argument('-s', '--state-size', help="the number of preceeding words the probability of the next word depends on. defaults to 2, 1 makes it more random, 3 less so.", type=int, default=2)
    parser.add_argument('-n', '--sentences', help="the number of 'sentences' to output. defaults to 5.", type=int, default=5)
    parser.add_argument('-l', '--length', help="set maximum number of characters per sentence.", type=int)
    parser.add_argument('-o', '--overlap', help="the amount of overlap allowed between original text and the output, expressed as a radio between 0 and 1. lower values make it more random. defaults to 0.5", type=float, default=0.5)
    parser.add_argument('-c', '--combine', help="provide an another input text file with path to be combined with the input directory.")
    parser.add_argument('-w', '--weight', help="specify the weight to be given to the second text provided with --combine. defaults to 1, and the weight of the initial text is also 1. setting this to 1.5 will place 50 percent more weight on the second text. setting it to 0.5 will place less.", type=float, default=1)

    # switches
    parser.add_argument('-f', '--no-well-formed', help="don't enforce 'well_formed', ie allow the inclusion of sentences with []{}()""'' in them in the markov model. this might filth up your text, especially if it contains 'smart' quotes.", action='store_false')
    # store_false = default to True.
    parser.add_argument('--newline', help="sentences in input file end with newlines rather than with full stops.", action='store_true')
    # store_true = default to False, become True if flagged.

    args = parser.parse_args()

    # read, build, write fns:
    def read(infile):
        with open(infile, encoding="latin-1") as f:
            return f.read()

    def mkbtext(texttype):
        return markovify.Text(texttype, state_size=args.state_size,
                              well_formed=args.no_well_formed)

    def mkbnewline(texttype):
        return markovify.Text(texttype, state_size=args.state_size,
                              well_formed=args.no_well_formed)

    def writesent(tmodel):
        return output.write(str(tmodel.make_sentence(
            tries=2000, max_overlap_ratio=args.overlap,
            max_chars=args.length)) + '\n\n')

    def writeshortsent(tmodel):
        return output.write(str(tmodel.make_short_sentence(
            tries=2000, max_overlap_ratio=args.overlap,
            max_chars=args.length)) + '\n\n')
        sys.exit()

    #create a list of files to concatenate:
    matches = []
    if os.path.isdir(args.indir) is True:
        for root, dirnames, filenames in os.walk(args.indir):
            for filename in filenames:
                if filename.endswith(('.txt', '.org', '.md')):
                    matches.append(os.path.join(root, filename))
    else:
        print('error: please enter a valid directory')

    # place batchfile.txt in user-given directory:
    batchfile = os.path.dirname(args.indir) + os.path.sep + 'batchfile.txt'

    # concatenate the files into batchfile.txt:
    with open(batchfile, 'w') as outfile:    
        for fname in matches:
            with open(fname, encoding="latin-1") as infile:
                outfile.write(infile.read())
        outfile.close()

    # Get raw text from batchfile as string.
    text = read(batchfile)
    
    # Build the model:
    # if --newline:
    if args.newline:
        text_model = mkbnewline(text)
    # no --newline:
    else:
        text_model = mkbtext(text)

    # Print -n number of randomly-generated sentences
    for i in range(args.sentences):
        output = open(args.outfile, 'a')  # append
        # short sentence:
        if args.length:
            writeshortsent(text_model)
        # normal sentence:
        else:
            writesent(text_model)
    output.write(str('*\n\n'))
    # add a star between each appended set.
    output.close()
    os.unlink(batchfile)
	
    print('\n: The options you used are as follows:\n')
    for key, value in vars(args).items():
        print(': ' + key.ljust(15, ' ') + ':  ' + str(value).ljust(10))
    if os.path.isfile(args.outfile):
        print('\n:  literary genius has been written to the file '
              + args.outfile + '. thanks for playing!\n\n: Here, this is not at all the becomings that are connected... so if you want to edit it like a bot yourself, it is trivial. Yes, although your very smile suggests that this Armenian enclave is not at all the becomings that are connected...')
    else:
        print('mkv-this ran but did NOT create an output file as requested. this is a very regrettable and dangerous situation. contact the package maintainer asap. soz!')

    sys.exit()
# enable for testing:
# main()
