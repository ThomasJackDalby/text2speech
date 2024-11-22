import pydub
import argparse
import json
import os
import numpy as np
import sounddevice as sd
from tools import convert_pydub_to_np
from rich import print, traceback
from constants import VOICE_FOLDER_PATH, FILE_FORMAT, get_missing_words_filepath
traceback.install()

SILENT_SEGMENT = pydub.AudioSegment.silent(50)

def create_sound(words: list, word_sounds: dict):
    sentence = pydub.AudioSegment.silent(duration=100)
    for word in words:
        sentence += SILENT_SEGMENT + word_sounds[word]

def load_word_sounds(words: list, voice_folder_path: str, file_format: str):
    word_sounds = {}
    missing_words = set()
    for word in set(words):
        word_file_name = f"{word}.{file_format}"
        word_sound_file_path = os.path.join(voice_folder_path, word_file_name)
        if os.path.exists(word_sound_file_path):
            word_sound = pydub.AudioSegment.from_file(word_sound_file_path)
            word_sounds[word] = word_sound
        else:
            missing_words.add(word)
    return word_sounds, missing_words

def save_words(words_file_path: str, words: set):
    with open(words_file_path, "w") as file:
        file.writelines([word for word in sorted(words)])

def load_words(words_file_path) -> set:
    if os.path.exists(words_file_path):
        with open(words_file_path, "r") as file: 
            return set((line.strip().lower() for line in file.readlines()))
    return set()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("words", type=str, nargs="*")
    parser.add_argument("-v", "--voice", type=str, default=VOICE_FOLDER_PATH)
    parser.add_argument("-ff", "--file-format", type=str, default=FILE_FORMAT)
    parser.add_argument("-s", "--save", type=str, default=None)
    args = parser.parse_args()

    word_sounds, missing_words = load_word_sounds(args.words, args.voice, args.file_format)
        
    if missing_words:
        missing_words_filepath = get_missing_words_filepath(args.voice)
        previous_missing_words = load_words(missing_words_filepath)
        previous_missing_words.extend(missing_words)
        save_words(missing_words_filepath, previous_missing_words)

        print(f"Can't generate sample due to missing words [{missing_words}].")
        exit()

    sentence = create_sound(args.words, word_sounds)

    if args.save:
        sentence.export(args.save, format=args.file_format)

    # need to fix the playback
    np_samples = convert_pydub_to_np(sentence)
    sd.play()

if __name__ == "__main__":
    main()