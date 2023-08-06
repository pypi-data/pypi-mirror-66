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
    a (very basic) script to markovify local and/or remote text files and
    output a user-specified number of sentences to a local text file.
    see --help for other options.
"""

import os
import requests
import markovify
import sys
import argparse
import html2text

# argparse
def parse_the_args():
    parser = argparse.ArgumentParser(prog="mkv-this", description="markovify one or two local or remote text files and output the results to a local text file.",
                                     epilog="may you find many prophetic énoncés in your virtual bird guts! Here, this is not at all the becomings that are connected... so if you want to edit it like a bot yourself, it is trivial.")

    # positional args:
    parser.add_argument(
        'infile', help="the text file to process. NB: file cannot be empty.")
    parser.add_argument('outfile', nargs='?', default="./mkv-output.txt",
                        help="the file to save to. if the file is used more than once, subsequent literature will be appended to it. defaults to ./mkv-output.txt.")

    # optional args:
    parser.add_argument('-s', '--state-size', help="the number of preceeding words used to calculate the probability of the next word. defaults to 2, 1 makes it more random, 3 less so. > 4 will likely have little effect.", type=int, default=2)
    parser.add_argument(
        '-n', '--sentences', help="the number of 'sentences' to output. defaults to 5.", type=int, default=5)
    parser.add_argument(
        '-l', '--length', help="set maximum number of characters per sentence.", type=int)
    parser.add_argument(
        '-o', '--overlap', help="the amount of overlap allowed between original and output, expressed as a ratio between 0 and 1. defaults to 0.5", type=float, default=0.5)
    parser.add_argument(
        '-c', '--combine', help="provide an another text file to be combined with the first item.")
    parser.add_argument('-C', '--combine-URL',
                        help="provide a URL to be combined with the first item")
    parser.add_argument('-w', '--weight', help="specify the weight to be given to the text provided with -c or -C. defaults to 1, and the weight of the initial text is 1. 1.5 will place more weight on the second text, 0.5 will place less.", type=float, default=1)

    # switches
    parser.add_argument(
        '-u', '--URL', help="infile is a URL instead.", action='store_true')
    parser.add_argument('-f', '--no-well-formed', help="don't enforce 'well_formed': allow the inclusion of sentences containing []{}()""'' in the markov model. might filth up your text, eg if it contains 'smart' quotes.", action='store_false')
    # store_false = default to True.
    parser.add_argument(
        '--newline', help="sentences in input file end with newlines \
        rather than full stops.", action='store_true')
    # store_true = default to False, become True if flagged.

    return parser.parse_args()

# fetch/read/build/write fns:


def URL(insert):
    try:
        req = requests.get(insert)
        req.raise_for_status()
    except Exception as exc:
        print(f': There was a problem: {exc}.\n: Please enter a valid URL')
        sys.exit()
    else:
        print(': fetched URL.')
        return req.text


def convert_html(html):
    h2t = html2text.HTML2Text()
    h2t.ignore_links = True
    h2t.ignore_images = True
    h2t.ignore_emphasis = True
    print(': URL converted to text')
    return h2t.handle(html)


def read(infile):
    try:
        with open(infile, encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(infile, encoding="latin-1") as f:
            return f.read()
    except FileNotFoundError:
        print(fnf)
        sys.exit()


def mkbtext(texttype):
    return markovify.Text(texttype, state_size=args.state_size,
                          well_formed=args.no_well_formed)


def mkbnewline(texttype):
    return markovify.NewlineText(texttype, state_size=args.state_size,
                                 well_formed=args.no_well_formed)


def writesentence(tmodel):
    for i in range(args.sentences):
        output = open(args.outfile, 'a')  # append
        # short:
        if args.length:
            output.write(str(tmodel.make_short_sentence(
                tries=2000, max_overlap_ratio=args.overlap,
                max_chars=args.length)) + '\n\n')
        # normal:
        else:
            output.write(str(tmodel.make_sentence(
                tries=2000, max_overlap_ratio=args.overlap,
                max_chars=args.length)) + '\n\n')
    output.write(str('*\n\n'))
    output.close()


# make args + fnf avail to all:
args = parse_the_args()
fnf = ': error: file not found. please provide a path to a really-existing \
    file!'


def main():
    # if a -c/-C, combine it w infile/URL:
    if args.combine or args.combine_URL:
        if args.combine:
            # get raw text as a string for both:
            #            try:
            # infile is URL:
            if args.URL:
                html = URL(args.infile)
                text = convert_html(html)
            # or normal:
            else:
                text = read(args.infile)
            # read -c file:
            ctext = read(args.combine)

        # if -C, combine it w infile/URL:
        elif args.combine_URL:
            #            try:
            # infile is URL:
            if args.URL:
                html = URL(args.infile)
                text = convert_html(html)
                # or normal:
            else:
                text = read(args.infile)
            # now combine_URL:
            html = URL(args.combine_URL)
            ctext = convert_html(html)

        # build the models + a combined model:
        # with --newline:
        if args.newline:
            text_model = mkbnewline(text)
            ctext_model = mkbnewline(ctext)
        # no --newline:
        else:
            text_model = mkbtext(text)
            ctext_model = mkbtext(ctext)

        combo_model = markovify.combine(
            [text_model, ctext_model], [1, args.weight])

        writesentence(combo_model)

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
            text_model = mkbnewline(text)
        # no --newline:
        else:
            text_model = mkbtext(text)

        writesentence(text_model)

    print('\n: The options you used are as follows:\n')
    for key, value in vars(args).items():
        print(': ' + key.ljust(15, ' ') + ':  ' + str(value).ljust(10))
    if os.path.isfile(args.outfile):
        print("\n:  literary genius has been written to the file "
              + args.outfile + ". thanks for playing!\n\n: 'Here, this is not at all the becomings that are connected... so if you want to edit it like a bot yourself, it is trivial. Yes, although your very smile suggests that this Armenian enclave is not at all the becomings that are connected...'")
    else:
        print(': mkv-this ran but did NOT create an output file as requested. this is a very regrettable and dangerous situation. contact the package maintainer asap. soz!')

    sys.exit()


# for testing:
if __name__ == '__main__':
    main()
