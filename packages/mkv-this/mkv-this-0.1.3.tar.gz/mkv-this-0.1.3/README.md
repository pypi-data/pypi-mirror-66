
## mkv-this

mkv-this is a little script that uses the `markovify` python module to output a bunch of bot sentences based on a bank of text that you feed it. the results are saved to a text file of your choosing. if you run it again on the same output file, the new results are appended after the old ones.

it was written by a total novice, so you probably shouldn’t download it.

#### install with pip:

you can install it with pip, the python package manager.

`python3 -m pip install mkv-this`

you need python3, and markovify is a dependency, but it should install with mkv-this.

#### help:

run `mkv-this -h` to see all the options and explanations of what they mean.

#### for best results:

feed `mkv-this` large-ish amounts of well punctuated text. it works best if you bulk replace/remove as much mess as possible (URLs, metadata, stars, bullets, etc.)

if your input text doesn’t have full-stops to mark the ends of sentences, trying putting each 'sentence' on a newline, so the parser doesn't read your entire file as one big sentence.

you’ll want to edit the output too. it is very much supposed to be a kind of raw material for further human editing, rather than print-ready bosh.

for further tips on basic output, see https://github.com/jsvine/markovify#basic-usage.

