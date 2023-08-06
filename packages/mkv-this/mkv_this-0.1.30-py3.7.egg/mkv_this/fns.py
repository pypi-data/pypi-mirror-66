import markovify
import sys
import requests
import argparse

    
def URL(insert): # WORKS!
     try:
         req = requests.get(insert) # URL is stored in infile.
         req.raise_for_status() # autob says always do this
     except Exception as exc:
         print(f'There was a problem: {exc}') # from autoboring
         sys.exit()
     else:
         print('text fetched from URL.') # NB unable to use "args.infile" here!
         return req.text # return so you can var this fn directly in main.
