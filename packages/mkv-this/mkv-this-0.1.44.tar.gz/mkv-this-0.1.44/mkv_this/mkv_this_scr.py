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
    a (very basic) script to markovify local files or URLs and
    output a user-specified number of sentences to a local text file.
"""

import os
import re
import requests
import markovify
import sys
import argparse
import html2text
import bs4

# argparse
def parse_the_args():
    parser = argparse.ArgumentParser(prog="mkv-this", description="markovify local text files or URLs and output the results to a local text file.",
                                     epilog="may you find many prophetic énoncés in your virtual bird guts! Here, this is not at all the becomings that are connected... so if you want to edit it like a bot yourself, it is trivial.")

    # positional args:
    parser.add_argument(
        'infile', help="the text file to process. NB: file cannot be empty.")
    parser.add_argument('outfile', nargs='?', default="./mkv-scr-output.txt",
                        help="the file to save to. if the file is used more than once, subsequent literature will be appended to it. defaults to ./mkv-output.txt.")

    # optional args:
    parser.add_argument('-s', '--state-size', help="the number of preceeding words used to calculate the probability of the next word. defaults to 2, 1 makes it more random, 3 less so. > 4 will likely have little effect.", type=int, default=2)
    parser.add_argument(
        '-n', '--sentences', help="the number of 'sentences' to output. defaults to 5. NB: if your text has no initial caps, a 'sentence' will be a paragraph.", type=int, default=5)
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
    parser.add_argument('-g', '--Guardian', help="infile is a link to a Guardian World news page for a particular date, in the format 'https://theguardian.com/world/YYYY/mmm/dd'. (eg '/2020/apr/02'). all articles linked from that page will be used as input.", action='store_true')
    parser.add_argument('-f', '--well-formed', help="enforce 'well_formed': discard sentences containing []{}()""'' from the markov model. use if output is filthy.", action='store_true') # store_false = default to True.
    parser.add_argument(
        '--newline', help="sentences in input file end with newlines \
        rather than full stops.", action='store_true')
    # store_true = default to False, become True if flagged.

    return parser.parse_args()

# fetch/read/build/write fns:

### sraper fns for multiple URLS:


def get_urls(st_url):
#    st_url = 'https://theguardian.com/cat/YEAR/mth/xx' # starting URL format The Guardian
    try:
        req = requests.get(st_url)
        req.raise_for_status()
    except Exception as exc:
        print(f': There was a problem: {exc}.\n: Please enter a valid URL')
        sys.exit()
    else:
        print(': fetched initial URL.')
        soup = bs4.BeautifulSoup(req.text, "lxml")
        art_elem = soup.select('div[class="fc-item__header"] a[data-link-name="article"]') # pull the element containing article links.
        urls = []
        for i in range(len(art_elem)):
            urls = urls + [art_elem[i].attrs['href']]
        print(': fetched list of URLs')
        return urls # returns a LIST
        

def scr_URLs(urls): # input a LIST
    try:
        content = []
        for i in range(len(urls)):
            req = requests.get(urls[i])
            req.raise_for_status() # req not defined! dunno how to do this for each.
            content = content + [req.text] #[requests.get(urls[i]).text] # works but SUPER slow.
            print(': fetched page ' + urls[i])
    except Exception as exc:
        print(f': There was a problem: {exc}.\n: There was trouble in your list of URLs')
        sys.exit()
    else:
        # print(len(req))
        # content = []
        # for i in range(len(req)):
        #     content = content + [req.text]
        print(': fetched all pages.')
        return content

def scr_convert_html(content): # takes a LIST of html pages
    h2t = html2text.HTML2Text()
    h2t.ignore_links = True
    h2t.images_to_alt = True
    h2t.ignore_emphasis = True
    h2t.ignore_tables = True
    h2t.unicode_snob = True
    h2t.decode_errors = 'ignore'
    h2t.escape_all = False # remove all noise if needed
    s = []
    for i in range(len(content)):
        s = s + [h2t.handle(content[i])] # convert
    t = []
    for i in range(len(s)):
        t = t + [re.sub('[#*]', '', s[i])] # remove hash/star from the 'markdown'
    u = ' '.join(t) # convert list to string
    print(': Pages converted to text')
    return u


### normal URL functions:


def URL(insert):
    try:
        req = requests.get(insert)
        req.raise_for_status()
    except Exception as exc:
        print(f': There was a problem: {exc}.\n: Please enter a valid URL')
        sys.exit()
    else:
        print(': fetched html page.')
        return req.text


def convert_html(html):
    h2t = html2text.HTML2Text()
    h2t.ignore_links = True
    h2t.images_to_alt = True
    h2t.ignore_emphasis = True
    h2t.ignore_tables = True
    h2t.unicode_snob = True
    h2t.decode_errors = 'ignore'
    h2t.escape_all = False # remove all noise if needed
    s = h2t.handle(html)
    s = re.sub('[#*]', '', s) # remove hashes and stars from the 'markdown'
    print(': html converted to text')
    return s


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


def mkbtext(texttype, args_ss, args_wf):
    return markovify.Text(texttype, state_size=args_ss,
                          well_formed=args_wf)


def mkbnewline(texttype, args_ss, args_wf):
    return markovify.NewlineText(texttype, state_size=args_ss,
                                 well_formed=args_wf)


def writesentence(tmodel, args_sen, args_out, args_over, args_len):
    for i in range(args_sen):
        output = open(args_out, 'a')  # append
        # short:
        if args.length:
            output.write(str(tmodel.make_short_sentence(
                tries=2000, max_overlap_ratio=args_over,
                max_chars=args_len)) + '\n\n')
        # normal:
        else:
            output.write(str(tmodel.make_sentence(
                tries=2000, max_overlap_ratio=args_over,
                max_chars=args_len)) + '\n\n')
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
            # or URL set:
            elif args.Guardian:
                urls = get_urls(args.infile)
                html = scr_URLs(urls)
                text = scr_convert_html(html)
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
            # or URL set:
            elif args.Guardian:
                urls = get_urls(args.infile)
                html = scr_URLs(urls)
                text = scr_convert_html(html)
            # or normal:
            else:
                text = read(args.infile)
            # now combine_URL:
            html = URL(args.combine_URL)
            ctext = convert_html(html)

        # build the models + a combined model:
        # with --newline:
        if args.newline:
            text_model = mkbnewline(text, args.state_size, args.well_formed)
            ctext_model = mkbnewline(ctext, args.state_size, args.well_formed)
        # no --newline:
        else:
            text_model = mkbtext(text, args.state_size, args.well_formed)
            ctext_model = mkbtext(ctext, args.state_size, args.well_formed)

        combo_model = markovify.combine(
            [text_model, ctext_model], [1, args.weight])

        writesentence(combo_model, args.sentences, args.outfile, args.overlap, args.length)

    # if no -c/-C, do normal:
    else:
        # Get raw text as string.
        # either URL:
        if args.URL:
            html = URL(args.infile)
            text = convert_html(html)
        # or URL set:
        elif args.Guardian:
            urls = get_urls(args.infile)
            html = scr_URLs(urls)
            text = scr_convert_html(html)
        # or local:
        else:
            text = read(args.infile)

        # Build the model:
        # if --newline:
        if args.newline:
            text_model = mkbnewline(text, args.state_size, args.well_formed)
        # no --newline:
        else:
            text_model = mkbtext(text, args.state_size, args.well_formed)

        writesentence(text_model, args.sentences, args.outfile, args.overlap, args.length)

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
