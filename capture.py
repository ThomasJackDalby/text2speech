# capture.py
# Guides the user through recording words and processes the files to be used in the generate method.

import sounddevice as sd
import pydub
import json
import io
import os
import scipy.io.wavfile
import argparse

DEFAULT_DURATION = 2
FREQUENCY = 16000
DEFAULT_TARGET_FOLDER_PATH = "raw"
DEFAULT_FILE_FORMAT = "mp3"

sd.default.samplerate = FREQUENCY
sd.default.channels = 1

def save_word_sound(
        file_path, 
        word, 
        recording,
        file_format = DEFAULT_FILE_FORMAT):
    with io.BytesIO() as wav_io:
        scipy.io.wavfile.write(wav_io, FREQUENCY, recording)
        wav_io.seek(0)
        sound = pydub.AudioSegment.from_wav(wav_io)
        sound.export(file_path, format=file_format)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--words", type=str)
    args = parser.parse_args()

    with open(args.words, "r") as file:
        words = [line.strip().lower() for line in file.readlines()]

    for word in words:
        print(f"Say '{word}'")
        continue
        word_sound = sd.rec(int(DEFAULT_DURATION * FREQUENCY))
        sd.wait()

        file_name = f"{word}.{DEFAULT_FILE_FORMAT}"
        file_path = os.path.join(DEFAULT_TARGET_FOLDER_PATH, file_name)
        save_word_sound(file_path, word, word_sound)
        