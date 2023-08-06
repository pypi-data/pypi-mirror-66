import os
import re
import requests
import markovify
import sys
import argparse
import html2text

fnf = ': error: file not found. please provide a path to a really-existing file!'


def URL(insert):
    """ fetch a url """
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
    """ convert a fetched page to text """
    h2t = html2text.HTML2Text()
    h2t.ignore_links = True
    h2t.images_to_alt = True
    h2t.ignore_emphasis = True
    h2t.ignore_tables = True
#    h2t.unicode_snob = True
    h2t.decode_errors = 'ignore'
    h2t.escape_all = False # remove all noise if needed
    print(': URL converted to text')
    s = h2t.handle(html)
    s = re.sub('[#*]', '', s) # remove hashes and stars from the 'markdown'
    return s


def read(infile):
    """ read your (local) file for the markov model """
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
    """ build a markov model """
    return markovify.Text(texttype, state_size=args_ss,
                          well_formed=args_wf)


def mkbnewline(texttype, args_ss, args_wf):
    """ build a markov model, newline """
    return markovify.NewlineText(texttype, state_size=args_ss,
                                 well_formed=args_wf)


def writeshortsentence(tmodel, args_sen, args_out, args_over, args_len):
    """ actually make the damn litter-atchya """
    for i in range(args_sen):
        output = open(args_out, 'a')  # append
        output.write(str(tmodel.make_short_sentence(
            tries=2000, max_overlap_ratio=args_over,
            max_chars=args_len)) + '\n\n')
    output.write(str('*\n\n'))
    output.close()


def writesentence(tmodel, args_sen, args_out, args_over, args_len):
    """ actually make the damn litter-atchya, and short """
    for i in range(args_sen):
        output = open(args_out, 'a')  # append
        output.write(str(tmodel.make_sentence(
            tries=2000, max_overlap_ratio=args_over,
            max_chars=args_len)) + '\n\n')
    output.write(str('*\n\n'))
    output.close()


### functions for mkv_this_scr.py

def get_urls(st_url):
    """ fetch a bunch of article URLs from The Guardian world news page for a given date. Format: 'https://theguardian.com/cat/YEAR/mth/xx' """
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
    """ actually fetch all the URLs obtained by get_urls """
    try:
        content = []
        for i in range(len(urls)):
            req = requests.get(urls[i])
            req.raise_for_status()
            content = content + [req.text] # SUPER slow.
            print(': fetched page ' + urls[i])
    except Exception as exc:
        print(f': There was a problem: {exc}.\n: There was trouble in your list of URLs')
        sys.exit()
    else:
        print(': fetched all pages.')
        return content

    
def scr_convert_html(content): # takes a LIST of html pages
    """ convert all pages obtained by scr_URLs """
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
