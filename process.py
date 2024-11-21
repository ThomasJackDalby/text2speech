# process.py
# takes any words in raw and removes silence, normalises the volume etc
import os
import json
import argparse
from pydub import AudioSegment, silence
import matplotlib.pyplot as plt
from rich import print, traceback
traceback.install()

FRAME_RATE = 16000
DEFAULT_RAW_FOLDER_PATH = "raw"
DEFAULT_PLOTS_FOLDER_PATH = "plots"
DEFAULT_PROCESSED_FOLDER_PATH = "processed"
DEFAULT_FILE_FORMAT = "mp3"
SUPPORTED_FILE_EXTENSIONS = [".mp3"]

def process_word(raw_sample, word):
    sample = raw_sample.set_frame_rate(16000)
    chunks = silence.detect_silence(sample, min_silence_len=100, silence_thresh = -50)
    plot(sample, chunks, word)

    if chunks[0][0] != 0: print("First silence is not at beginning.")
    if chunks[-1][1] != len(sample): print("Last silence is not at end.")
    return sample[chunks[0][1]:chunks[-1][0]]

def plot(sample, chunks, word):
    samples = sample.get_array_of_samples()
    plt.clf()
    plt.plot(samples)
    for chunk in chunks:
        plt.axvline(chunk[0] / 1000 * FRAME_RATE, color="green")
        plt.axvline(chunk[1] / 1000 * FRAME_RATE, color="red")
    #plt.show()
    #plt.savefig(f"{word}.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--raw", type=str, default=DEFAULT_RAW_FOLDER_PATH)
    parser.add_argument("-p", "--processed", type=str, default=DEFAULT_PROCESSED_FOLDER_PATH)
    parser.add_argument("-f", "--force", action='store_true', default=False)
    args = parser.parse_args()

    for folder_path, folder_names, file_names in os.walk(args.raw):
        for file_name in file_names:
            file_name_no_ext, file_ext = os.path.splitext(file_name)
            if not file_ext in SUPPORTED_FILE_EXTENSIONS:
                print(f"Skipped '{file_name}' as '{file_ext}' not a supported file extension.")     
                continue

            raw_file_path = os.path.join(folder_path, file_name)
            processed_file_name = f"{file_name_no_ext}.{DEFAULT_FILE_FORMAT}"
            processed_file_path = os.path.join(args.processed, processed_file_name)
            if not args.force and os.path.exists(processed_file_path):
                print(f"Skipped '{file_name}' as already processed.")
                continue
            print(f"Processing '{file_name}'")
     
            raw_sample = AudioSegment.from_file(raw_file_path)
            processed_sample = process_word(raw_sample, file_name_no_ext)
            processed_sample.export(processed_file_path, format=DEFAULT_FILE_FORMAT)