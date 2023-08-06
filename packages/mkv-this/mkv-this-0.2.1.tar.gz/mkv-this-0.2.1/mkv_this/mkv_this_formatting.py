#! /usr/bin/env python3

"""
    mkv-this: input text and/or url, output markovified text.

    Copyright (C) 2020 martianhiatus@riseup.net.

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


import markovify
import os
import sys
import argparse
from functions import (
    URL,
    convert_html,
    read,
    mkbtext,
    mkbnewline,
    writesentence,
    writeshortsentence,
)

# argparse


def parse_the_args():
    parser = argparse.ArgumentParser(
        prog="mkv-this",
        description=(
            "markovify local text files or URLs and output the results"
            "to a local text file."
        ),
        epilog=(
            "may you find many prophetic énoncés in your virtual bird guts!"
            "Here, this is not at all the becomings that are connected..."
            "so if you want to edit it like a bot yourself, it is trivial."
        ),
    )
    # positional args:
    parser.add_argument(
        "infile",
        help="the text file to process. NB: file cannot be empty."
    ),
    parser.add_argument(
        "outfile",
        nargs="?",
        default="./mkv-output.txt",
        help="the file to save to. if the file is used more than once, subsequent literature will be appended to it. defaults to ./mkv-output.txt.",
    ),
    # optional args:
    parser.add_argument(
        "-s",
        "--state-size",
        help="the number of preceeding words used to calculate the probability of the next word. defaults to 2, 1 makes it more random, 3 less so. > 4 will likely have little effect.",
        type=int,
        default=2,
    ),
    parser.add_argument(
        "-n",
        "--sentences",
        help="the number of 'sentences' to output. defaults to 5. NB: if your text has no initial caps, a 'sentence' will be a paragraph.",
        type=int,
        default=5,
    ),
    parser.add_argument(
        "-l",
        "--length",
        help="set maximum number of characters per sentence.",
        type=int,
    ),
    parser.add_argument(
        "-o",
        "--overlap",
        help="the amount of overlap allowed between original and output, expressed as a ratio between 0 and 1. defaults to 0.5",
        type=float,
        default=0.5,
    ),
    parser.add_argument(
        "-c",
        "--combine",
        help="provide an another text file to be combined with the first item.",
    ),
    parser.add_argument(
        "-C", "--combine-URL", help="provide a URL to be combined with the first item"
    ),
    parser.add_argument(
        "-w",
        "--weight",
        help="specify the weight to be given to the text provided with -c or -C. defaults to 1, and the weight of the initial text is 1. 1.5 will place more weight on the second text, 0.5 will place less.",
        type=float,
        default=1,
    ),

    # switches
    parser.add_argument(
        "-u", "--URL", help="infile is a URL instead.", action="store_true"
    ),
    # store_false = default to True.
    parser.add_argument(
        "-f",
        "--well-formed",
        help="enforce 'well_formed': discard sentences containing []{}()"
        "'' from the markov model. use if output is filthy.",
        action="store_true",
    ),
    parser.add_argument(
        "--newline",
        help="sentences in input file end with newlines \
        rather than full stops.",
        action="store_true",
    ),
    # store_true = default to False, become True if flagged.

    return parser.parse_args()


# make args avail:
args = parse_the_args()

# optional abbreviations:
a = vars(args)
inf = a['infile']
out = a['outfile']
wf = a['well_formed']
ss = a['state_size']
ov = a['overlap']
l = a['length']
s = a['sentences']
w = a['weight']


def main():
    # if a -c/-C, combine it w infile/URL:
    if args.combine or args.combine_URL:
        if args.combine:
            # get raw text as a string for both:
            # infile is URL:
            if args.URL:
                html = URL(inf) #args.infile)
                text = convert_html(html)
                # or normal:
            else:
                text = read(inf) #args.infile)
            # read -c file:
            ctext = read(args.combine)

        # if -C, combine it w infile/URL:
        elif args.combine_URL:
            # infile is URL:
            if args.URL:
                html = URL(inf) #args.infile)
                text = convert_html(html)
                # or normal:
            else:
                text = read(inf) #args.infile)
            # now combine_URL:
            html = URL(args.combine_URL)
            ctext = convert_html(html)

        # build the models + a combined model:
        # with --newline:
        if args.newline:
            text_model = mkbnewline(text, ss, wf) # args.state_size, args.well_formed)
            ctext_model = mkbnewline(ctext, ss, wf) # args.state_size, args.well_formed)
        # no --newline:
        else:
            text_model = mkbtext(text, ss, wf) # args.state_size, args.well_formed)
            ctext_model = mkbtext(ctext, ss, wf) # args.state_size, args.well_formed)

        combo_model = markovify.combine([text_model, ctext_model], [1, w]) # args.weight])

        # write it combo!
        if args.length:
            writeshortsentence(
                combo_model, s, out, ov, l) # args.sentences, args.outfile, #args.overlap, args.length
#            )
        else:
            writesentence(
                combo_model, s, out, ov, l) # args.sentences, args.outfile, #args.overlap, args.length
#            )

    # if no -c/-C, do normal:
    else:
        # Get raw text as string.
        # either URL:
        if args.URL:
            html = URL(args.infile)
            text = convert_html(html)
        # or local:
        else:
            text = read(args.infile)

        # Build the model:
        # if --newline:
        if args.newline:
            text_model = mkbnewline(text, ss, wf) # args.state_size, args.well_formed)
        # no --newline:
        else:
            text_model = mkbtext(text, ss, wf) # args.state_size, args.well_formed)

        # write it!
        if args.length:
            writeshortsentence(
                text_model, s, out, ov, l) # args.sentences, args.outfile, #args.overlap, args.length
 #           )
        else:
            writesentence(
                text_model, s, out, ov, l) # args.sentences, args.outfile, #args.overlap, args.length
#            )

    print("\n:                :\n")
    for key, value in vars(args).items():
        print(": " + key.ljust(15, " ") + ":  " + str(value).ljust(10))
    if os.path.isfile(args.outfile):
        print(
            "\n:  literary genius has been written to the file "
            + args.outfile
            + ". thanks for playing!\n\n: 'Here, this is not at all the becomings that are connected... so if you want to edit it like a bot yourself, it is trivial. Yes, although your very smile suggests that this Armenian enclave is not at all the becomings that are connected...'"
        )
    else:
        print(
            ": mkv-this ran but did NOT create an output file as requested. this is a very regrettable and dangerous situation. contact the package maintainer asap. soz!"
        )

    sys.exit()


if __name__ == "__main__":
    main()
