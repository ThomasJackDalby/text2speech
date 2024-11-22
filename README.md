# text2speech

A semi-crude test-to-speech engine in Python, written primarily to generate amusing sound bites for discord.

## How it works

text2speech is essentially a word (or generic sound) concatenation engine. It simply enables the generation of a sentence or phrase, by gluing together individually recorded words. There is a bit of processing, in the tidying up of the recordings, and adding in additional silence between words etc, but that's pretty much it.

It's written in Python, utilising a few 3rd party sound libraries (see the requirements.txt), and comprises a few scripts:

- 'capture.py' helps record large numbers of words 'quickly'.
- 'process.py' tidies up these crude recordings.
- 'talk.py' generates the output phrase.

## Getting started

First clone the repository locally, then change directory into it.

```
git clone https://github.com/ThomasJackDalby/text2speech.git
cd ./text2speech
```

As with all Python projects, using a virtual environment of some type is highly recommended to avoid package conflicts. Below is an example of doing this with the 'venv' module.

```
python -m venv .venv
.venv/scripts/activate
```

Install the required packages.

```
pip install -r ./requirements.txt
```

Note, pydub requires a 3rd party sound processing application such as ffmpeg, which is not installed automatically alongside the python module. Refer to the pydub project page for more info. If you choose to use ffmpeg, you can easily install it with chocolatey.

```
choco install ffmpeg-full
```

## Recording a voice

Before a phrase can be generated, the building block word sound bites need to be recorded. There are two approaches to this:

1. Only record the words you need, as and when you need them. The word repository will slowly grow over time through use.
2. Record a large set of common words up-front.

[1000-most-common-words.txt](https://raw.githubusercontent.com/powerlanguage/word-lists/refs/heads/master/1000-most-common-words.txt)


