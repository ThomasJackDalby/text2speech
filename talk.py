import pydub
import argparse
import json
import os
import numpy as np
import sounddevice as sd
from tools import convert_pydub_to_np
from rich import print, traceback
traceback.install()

WORD_SOUNDS_REPO_PATH = "processed"
MISSING_WORDS_FILEPATH = "missing_words.txt"
SILENT_SEGMENT = pydub.AudioSegment.silent(50)

def main():
    # get the sentence from the args
    parser = argparse.ArgumentParser()
    parser.add_argument("words", type=str, nargs="*")
    parser.add_argument("-s", "--save", type=str, default=None)
    args = parser.parse_args()

    # get word sounds from the repository
    word_sounds = {}
    missing_words = set()
    for word in set(args.words):
        word_sound_file_path = os.path.join(WORD_SOUNDS_REPO_PATH, f"{word}.mp3")
        if os.path.exists(word_sound_file_path):
            word_sound = pydub.AudioSegment.from_file(word_sound_file_path)
            word_sounds[word] = word_sound
        else:
            missing_words.add(word)
        
    if missing_words:
        if os.path.exists(MISSING_WORDS_FILEPATH):
            with open(MISSING_WORDS_FILEPATH, "r") as file: 
                missing_words_data = json.load(file)
        else:
            missing_words_data = []

        for word in missing_words:
            if word not in missing_words_data:
                missing_words_data.append(word)
        missing_words_data.sort()

        with open(MISSING_WORDS_FILEPATH, "w") as file:
            json.dump(missing_words_data, file)

        print(f"Can't generate sample due to missing words [{missing_words}].")
        exit()

    # glue the words together and save
    sentence = pydub.AudioSegment.silent(duration=100)
    for word in args.words:
        sentence += SILENT_SEGMENT + word_sounds[word]

    if args.save:
        sentence.export(args.save, format="mp3")

    np_samples = convert_pydub_to_np(sentence)
    sd.play()

if __name__ == "__main__":
    main()