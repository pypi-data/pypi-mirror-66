#! /home/mouse/nextcloud/python/venv/bin/python3

"""
    mkv-this: input text, output markovified text.
    Copyright (C) 2020 martian hiatus.

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
a (very basic) script to process a text file with markovify and
output a user-specified number sentences and state-size to a text file. see --help for other options.

TODO: allow -c to be called multiple times!
"""

import markovify
import sys
import argparse

# argparse for cmd line args
parser = argparse.ArgumentParser()

# positional args:
parser.add_argument('infile', help="the text file to process, with path. NB: file cannot be empty.")
parser.add_argument('outfile', nargs='?', default="./mkv-output.txt", help="the file to save to, with path. if the file is used more than once, subsequent literature will be appended to the file after a star. defaults to ./mkv-output.txt.")

# optional args:
parser.add_argument('-s', '--statesize', help="the number of preceeding words the probability of the next word depends on. defaults to 2, 1 makes it more random, and 3 less so.", type=int, default=2)
# if i use --state-size (w a dash) instead, the type=int doesn't work... not sure how to fix.
parser.add_argument('-n', '--sentences', help="the number of 'sentences' to output. defaults to 5.", type=int, default=5)
parser.add_argument('-c', '--combine', help="provide an another input text file with path to be combined with the first.")
parser.add_argument('-l', '--length', help="set maximum number of characters per sentence.", type=int)

args = parser.parse_args()

### just for testing:
# print(args.infile, args.outfile)
# print(args.infile)
# print(type(args.statesize))
# print(type(args.sentences))
# print(statesize)
# print(type(statesize))
# sys.exit()

# if a combine file isprovided, combine it w/ input file:
if args.combine :
    # get raw text as a string for both files:
    with open(args.infile) as f:
        text = f.read()

    with open(args.combine) as cf:
        ctext = cf.read()

    #build the models and build a combined model:
    text_model = markovify.Text(text, state_size=args.statesize)
    ctext_model = markovify.Text(ctext, state_size=args.statesize)

    combo_model = markovify.combine([text_model, ctext_model])

    # Print -n number of randomly-generated sentences
    for i in range(args.sentences):
        output = open(args.outfile, 'a')  # append
        if args.length :
            output.write(str(combo_model.make_short_sentence(args.length, tries=50, max_overlap_ratio=20)))
        else:
            output.write(str(combo_model.make_sentence(
                tries=50, max_overlap_ratio=20)) + '\n \n')
        # add newline between each sentence.
    output.write(str(' \n \n * \n \n'))
    # add a star between each appended set.
    output.close()

# if no combo file, just do normal:
else:
# Get raw text as string.
    with open(args.infile) as f:
        text = f.read()
        
    # Build the model:
    # NB: this errors if infile is EMPTY:
    text_model = markovify.Text(text, state_size=args.statesize) # arg 4, default=2

    # Print -n number of randomly-generated sentences
    for i in range(args.sentences):
        output = open(args.outfile, 'a')  # append to file
        if args.length :
            output.write(str(text_model.make_short_sentence(args.length, tries=50, max_overlap_ratio=20)))
        else:
            output.write(str(text_model.make_sentence(
                tries=50, max_overlap_ratio=20)) + '\n \n')
        # \n to add newline between each sentence.
    output.write(str(' \n \n * \n \n'))
    # add a star between each appended set.
    output.close()

print('\n:  literary genius has been written to the file ' + args.outfile + '. thanks for playing!')

sys.exit()
