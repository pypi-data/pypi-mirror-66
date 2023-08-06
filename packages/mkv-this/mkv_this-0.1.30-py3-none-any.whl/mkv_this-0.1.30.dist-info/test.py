import argparse

# argparse for cmd line args
parser = argparse.ArgumentParser()

# positional args:
# parser.add_argument('infile', help="the text file to process, with path. NB: file cannot be empty.")
# parser.add_argument('outfile', nargs='?', default="./mkv-output.txt", help="the file to save to, with path. if the file is used more than once, subsequent literature will be appended to the file after a star. defaults to ./mkv-output.txt.")

# optional args:
parser.add_argument('-s', '--state-size', help="the number of preceeding words used to calculate the probability of the next word. defaults to 2, 1 makes it more random, 3 less so. must be an integer. anything more than 4 will likely have little effect.", type=int, default=2)
# if i use --state-size (w a dash), type=int doesn't work.
parser.add_argument('-n', '--sentences', help="the number of 'sentences' to output. defaults to 5. must be an integer.", type=int, default=5)
parser.add_argument('-l', '--length', help="set maximum number of characters per sentence. must be an integer.", type=int)
parser.add_argument('-o', '--overlap', help="the amount of overlap allowed between original text and the output, expressed as a ratio between 0 and 1. defaults to 0.5", type=float, default=0.5)
parser.add_argument('-m', '--malformed', help="disable the inclusion of only 'well-formed' sentences, i.e. thouse without []{}()"", in the markov model.", action='store_false') # store_false = default value is True.
parser.add_argument('--newline', help="sentences in input file end with newlines rather than with full stops.", action='store_true') # store_true means default to False, and becomes True if flagged.
parser.add_argument('-c', '--combine', help="provide an another input text file with path to be combined with the first.")
parser.add_argument('-w', '--weight', help="specify the weight to be given to the second text provided with --combine. defaults to 1, and the weight of the initial text is also 1. setting this to 1.5 will place 50 percent more weight on the second text, while setting it to 0.5 will place less.", type=float, default=1)

args = parser.parse_args()

print(args)
print(type(args.state_size))
