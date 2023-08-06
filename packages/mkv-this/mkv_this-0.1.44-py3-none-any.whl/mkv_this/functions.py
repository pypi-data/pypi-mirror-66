import os
import re
import requests
import markovify
import sys
import html2text


fnf = ": error: file not found. please provide a path to a really-existing file!"


def URL(insert):
    """ fetch a url """
    try:
        req = requests.get(insert)
        req.raise_for_status()
        req.encoding = req.apparent_encoding
        # use chardet to catch encoding issue with ISO-8859-1/Latin-1.
    except Exception as exc:
        print(f": There was a problem: {exc}.\n: Please enter a valid URL")
        sys.exit()
    else:
        print(": fetched URL.")
        return req.text


def convert_html(html):
    """ convert a fetched page to text """
    h2t = html2text.HTML2Text()
    h2t.images_to_alt = True
    h2t.ignore_links = True
    h2t.ignore_emphasis = True
    h2t.ignore_tables = True
    h2t.unicode_snob = False
    h2t.decode_errors = "replace"
    h2t.escape_all = False  # remove all noise if needed
    s = h2t.handle(html)
    s = re.sub("[#*]", "", s)  # remove hashes and stars from the 'markdown'
    print(": URL converted to text")
    return s


def read(infile):
    """ read your (local) file for the markov model """
    try:
        with open(infile, encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(infile, encoding="latin-1") as f:
            return f.read()
    except IsADirectoryError as exc:
        print(
            f": There was a problem: {exc}.\n: Looks like you entered a directory. Use '-d' for that."
        )
        sys.exit()
    except FileNotFoundError:
        print(fnf)
        sys.exit()


def mkbtext(texttype, args_ss, args_wf):
    """ build a markov model """
    return markovify.Text(texttype, state_size=args_ss, well_formed=args_wf)


def mkbnewline(texttype, args_ss, args_wf):
    """ build a markov model, newline """
    return markovify.NewlineText(texttype, state_size=args_ss, well_formed=args_wf)


def writeshortsentence(tmodel, args_sen, args_out, args_over, args_len):
    """ actually make the damn litter-atchya """
    for i in range(args_sen):
        output = open(args_out, "a")  # append
        output.write(
            str(
                tmodel.make_short_sentence(
                    tries=2000, max_overlap_ratio=args_over, max_chars=args_len
                )
            )
            + "\n\n"
        )
    output.write(str("*\n\n"))
    output.close()


def writesentence(tmodel, args_sen, args_out, args_over, args_len):
    """ actually make the damn litter-atchya, and short """
    for i in range(args_sen):
        output = open(args_out, "a")  # append
        output.write(
            str(
                tmodel.make_sentence(
                    tries=2000, max_overlap_ratio=args_over, max_chars=args_len
                )
            )
            + "\n\n"
        )
    output.write(str("*\n\n"))
    output.close()


# functions for directory:
def dir_list(directory):
    # create a list of files to concatenate:
    matches = []
    if os.path.isdir(directory) is True:
        for root, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith((".txt", ".org", ".md")):
                    matches.append(os.path.join(root, filename))
        print(": text files fetched and combined")
    else:
        print(": error: please enter a valid directory")
        sys.exit()
    return matches  # returns a LIST of filenames


# feed this one the matches list:
def dir_cat(matchlist, batchfile):
    # concatenate into batchfile.txt:
    with open(batchfile, "w") as outfile:
        for fname in matchlist:
            try:
                with open(fname, encoding="utf-8") as infile:
                    outfile.write(infile.read())
            except UnicodeDecodeError:
                with open(fname, encoding="latin-1") as infile:
                    outfile.write(infile.read())
