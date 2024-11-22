# capture.py
# Guides the user through recording words and processes the files to be used in the generate method.

import sounddevice as sd
import pydub
import json
import io
import os
import scipy.io.wavfile
import argparse
from constants import RAW_FOLDER_PATH, FRAME_RATE, FILE_FORMAT, SUPPORTED_FILE_EXTENSIONS

DEFAULT_DURATION = 2

sd.default.samplerate = FRAME_RATE
sd.default.channels = 1

def save_word_sound(
        file_path, 
        word, 
        recording,
        file_format = FILE_FORMAT):
    with io.BytesIO() as wav_io:
        scipy.io.wavfile.write(wav_io, FRAME_RATE, recording)
        wav_io.seek(0)
        sound = pydub.AudioSegment.from_wav(wav_io)
        sound.export(file_path, format=file_format)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("words", type=str)
    parser.add_argument("-r", "--raw", type=str, default=RAW_FOLDER_PATH)
    parser.add_argument("-d", "--duration", type=int, default=DEFAULT_DURATION)
    parser.add_argument("-ff", "--file-format", type=str, default=FILE_FORMAT)
    parser.add_argument("-fr", "--frame-rate", type=int, default=FRAME_RATE)
    args = parser.parse_args()

    if args.file_format not in SUPPORTED_FILE_EXTENSIONS:
        print(f"'{args.file_format}' file format is not supported.")
        return
    
    with open(args.words, "r") as file:
        words = [line.strip().lower() for line in file.readlines()]

    number_of_samples = int(args.duration * args.frame_rate)
    for word in words:
        print(f"Say '{word}'")
        word_sound = sd.rec(number_of_samples)
        sd.wait()

        file_name = f"{word}.{args.file_format}"
        file_path = os.path.join(args.raw, file_name)
        save_word_sound(file_path, word, word_sound)

if __name__ == "__main__":
    main()
        