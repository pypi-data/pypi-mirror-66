#! /usr/bin/env python3

import markovify

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
