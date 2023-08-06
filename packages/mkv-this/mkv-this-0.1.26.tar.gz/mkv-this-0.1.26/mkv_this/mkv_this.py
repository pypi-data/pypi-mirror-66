#! /usr/bin/env python3

"""
    mkv-this: input text, output markovified text.
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
a (very basic) script to markovify a text file and
output a user-specified number of sentences to a text file. see --help for other options.
"""
   
     
import markovify
import sys
import argparse

def main():
    # argparse for cmd line args
    parser = argparse.ArgumentParser()

    # positional args:
    parser.add_argument('infile', help="the text file to process, with path. NB: file cannot be empty.")
    parser.add_argument('outfile', nargs='?', default="./mkv-output.txt", help="the file to save to, with path. if the file is used more than once, subsequent literature will be appended to the file after a star. defaults to ./mkv-output.txt.")

    # optional args:
    parser.add_argument('-s', '--state-size', help="the number of preceeding words used to calculate the probability of the next word. defaults to 2, 1 makes it more random, 3 less so. must be an integer. anything more than 4 will likely have little effect.", type=int, default=2)
    # if i use --state-size (w a dash), type=int doesn't work.
    parser.add_argument('-n', '--sentences', help="the number of 'sentences' to output. defaults to 5. must be an integer.", type=int, default=5)
    parser.add_argument('-l', '--length', help="set maximum number of characters per sentence. must be an integer.", type=int)
    parser.add_argument('-o', '--overlap', help="the amount of overlap allowed between original text and the output, expressed as a ratio between 0 and 1. defaults to 0.5", type=float, default=0.5)
    parser.add_argument('-f', '--no-well-formed', help="don't enforce 'well_formed', ie allow the inclusion of sentences with []{}()""'' in them in the markov model. this might filth up your text, especially if it contains 'smart' quotes.", action='store_false') # store_false = default to True.
    parser.add_argument('--newline', help="sentences in input file end with newlines rather than with full stops.", action='store_true')
    # store_true = default to False, become True if flagged.
    parser.add_argument('-c', '--combine', help="provide an another input text file with path to be combined with the first.")
    parser.add_argument('-w', '--weight', help="specify the weight to be given to the second text provided with --combine. defaults to 1, and the weight of the initial text is also 1. setting this to 1.5 will place 50 percent more weight on the second text, while setting it to 0.5 will place less.", type=float, default=1)

    args = parser.parse_args()

    # if a combine file is provided, combine it w/ input file:
    if args.combine :
        # get raw text as a string for both files:
        with open(args.infile, encoding="latin-1") as f:
            text = f.read()

        with open(args.combine, encoding="latin-1") as cf:
            ctext = cf.read()

        # build the models and build a combined model:
        # NB: attempting to implement Newline option here (and below):
        if args.newline :
            text_model = markovify.NewlineText(
                text, state_size=args.state_size, well_formed=args.no_well_formed)
            ctext_model = markovify.NewlineText(
                ctext, state_size=args.state_size, well_formed=args.no_well_formed)
        else:
            text_model = markovify.Text(text,
                state_size=args.state_size, well_formed=args.no_well_formed)
            ctext_model = markovify.Text(ctext,
                state_size=args.state_size, well_formed=args.no_well_formed)

        combo_model = markovify.combine([text_model, ctext_model], [1, args.weight])

        # Print -n number of randomly-generated sentences
        for i in range(args.sentences):
            output = open(args.outfile, 'a')  # appending
            if args.length :
                output.write(str(combo_model.make_short_sentence(
                    args.length, tries=2000, max_overlap_ratio=args.overlap)) + '\n \n')
            else:
                output.write(str(combo_model.make_sentence(
                    tries=2000, max_overlap_ratio=args.overlap)) + '\n \n')
                # add newline between each sentence.
        output.write(str(' \n \n * \n \n'))
        # add a star between each appended set.
        output.close()

        # if no combo file, just do normal:
    else:
        # Get raw text as string.
        with open(args.infile, encoding="latin-1") as f:
            text = f.read()
        
        # Build the model:
        # NB: this errors if infile is EMPTY:

        ## newline option:
        if args.newline :
            text_model = markovify.NewlineText(text,
                state_size=args.state_size, well_formed=args.no_well_formed)
        else:
            text_model = markovify.Text(text,
                state_size=args.state_size, well_formed=args.no_well_formed)

        # Print -n number of randomly-generated sentences
        for i in range(args.sentences):
            output = open(args.outfile, 'a')  # append to file
            if args.length :
                output.write(str(text_model.make_short_sentence(
                    args.length, tries=2000, max_overlap_ratio=args.overlap)) + '\n \n')
            else:
                output.write(str(text_model.make_sentence(
                    tries=2000, max_overlap_ratio=args.overlap)) + '\n \n')
                # \n to add newline between each sentence.
        output.write(str(' \n \n * \n \n'))
        # add a star between each appended set.
        output.close()

    print('\n:  literary genius has been written to the file ' + args.outfile + '. thanks for playing!')

    sys.exit()
