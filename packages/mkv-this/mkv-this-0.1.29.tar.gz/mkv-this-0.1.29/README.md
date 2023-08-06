
## disclaimer

i wrote this cli rapper for the `markovify` python module because i wanted its features to be available as a cli tool.

i only published it in case someone who actually knows what they're doing felt like picking it up and improving on it. (and to share it with friends.)

and if you are interested in fixing my amateur code, then by all means!

maybe this functionality already exists somewhere, but i couldn't find it. if it does, pls let me know!

## mkv-this

`mkv-this` is a little script that outputs a bunch of bot-like sentences based on a bank of text that you feed it. the results are saved to a text file. if you run it again with the same output file, the new results are appended after the old ones.

a second command, `mkv-this-dir` (see below) allows you to input a directory and it will read all text files within it as the input.

`mkv-this` simply makes some of the features of the excellent `markovify` module available as a command line tool. it was written by a total novice, so you probably shouldn’t download it. i only learned about `argparser` yesterday, and pypi.org today, no matter what day it is. tomorrow i might learn about `os` and `sys`. and then maybe even `cookiecutter`!

### installing

install it with `pip`, the python package manager:

`python3 -m pip install mkv-this`

or

`pip install mkv-this`

to do this you need `python3` and `pip`. if you don't have them, install them through your system's package manager. on debian (+ derivatives), for example, you'd run:

`sudo apt install python3 python3-pip`

`markovify` is also a dependency, but it should install along with `mkv-this`.

if you get sth like `ModuleNotFound error: No module named 'modulename'`, just run `pip install modulename` to get the missing module.

### repository

if you are reading this on pypi.org, the repo is here:
https://git.disroot.org/mousebot/mkv-this.

### macos

it seems to run on macos too.

you may already have python installed. if not, you first need to install [homebrew](https://brew.sh/#install), edit your PATH so that it works, then install `python3` with `brew install python3`. if you are already running an old version of `homebrew` you might need to run `brew install python3 && brew postinstall python3` to get `python3` and `pip` running right.

you can check if `pip` is installed with `pip --version`, or `pip3 --version`.

i know nothing about macs so if you ask me for help i'll just send you random copypasta from the interwebs.

### options

the script implements a few of the basic `markovify` options, so you can specify:

* how many sentences to output (default = 5)
* the state size, i.e. the number of preceeding words to be used in calculating the probability of the next word (default = 2).
* a maximum sentence length, in characters.
* the amount of (verbatim) overlap allowed between your input text and your output text.
* that your text's sentences end with newlines rather than full-stops.
* an additional file to use for text input. you can add only one. if you want to feed a stack of files into your bank, use `mkv-this-dir`.
* the relative weight to give to the second file if it is used.

as of 0.1.29 you can also specify:

* a URL to a text file online. (you can input something that isn't a text file but the results will be mush.)
* an additional URL to use as text input.

run `mkv-this -h` to see how to use these options.

### mkv-this-dir: markovify a directory of text files

`mkv-this` can only take two files as input material each time. if you want to input a stack of files, use `mkv-this-dir`. it allows you to specify a directory and all text files in it will be used as input material.

if for some reason you want to get a similar funtionality with `mkv-this`, you can easily concatenate some files yourself from the command line, then process them:

* copy all your text files into a directory
* cd into the directory
* run `cat * > outputfile.txt`
* run mkv-this on your newly created file: `mkv-this outputfile.txt`
* this approach has the benefit of creating a file with encoding that mkv-this can certainly handle.

### file types

you need to input plain text files. currently accepted file extensions are `.txt`, `.org` and `.md`. it is trivial to add others, so if you want one included just ask.

### for best results

feed `mkv-this` large-ish amounts of well punctuated text. it works best if you bulk replace/remove as much mess as possible (URLs, code, tags, metadata, stars, bullets, etc.), unless you want mashed versions of those things in your output.

you’ll probably want to edit the output. it is very much supposed to be a kind of raw material rather than print-ready boilerplate bosh, although many bots are happily publishing such output directly. you might find that it prompts you to edit it like a bot yourself.

for a few further tips, see https://github.com/jsvine/markovify#basic-usage.

happy zaning.
