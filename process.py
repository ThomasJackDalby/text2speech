# process.py
# takes any words in raw and removes silence, normalises the volume etc

import os
import argparse
from pydub import AudioSegment, silence
import matplotlib.pyplot as plt
from rich import print, traceback
from constants import VOICE_FOLDER_PATH, FRAME_RATE, RAW_FOLDER_PATH, PROCESSED_FOLDER_PATH, FILE_FORMAT, SUPPORTED_FILE_EXTENSIONS, PLOTS_FOLDER_PATH
traceback.install()

def process_word(raw_sample: AudioSegment, word: str, frame_rate: int, plots_folder_path: str, debug: bool = False):
    sample = raw_sample.set_frame_rate(frame_rate)
    chunks = silence.detect_silence(sample, min_silence_len=100, silence_thresh = -50)
    
    if debug:
        samples = sample.get_array_of_samples()
        plt.clf()
        plt.plot(samples)
        for chunk in chunks:
            plt.axvline(chunk[0] / 1000 * FRAME_RATE, color="green")
            plt.axvline(chunk[1] / 1000 * FRAME_RATE, color="red")
        plot_file_name = f"{word}.png"
        plot_file_path = os.path.join(plots_folder_path, plot_file_name)
        plt.savefig(plot_file_path)

    if chunks[0][0] != 0: print("First silence is not at beginning.")
    if chunks[-1][1] != len(sample): print("Last silence is not at end.")
    return sample[chunks[0][1]:chunks[-1][0]]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--voice", type=str, default=VOICE_FOLDER_PATH)
    parser.add_argument("-r", "--raw", type=str, default=RAW_FOLDER_PATH)
    parser.add_argument("-p", "--processed", type=str, default=PROCESSED_FOLDER_PATH)
    parser.add_argument("-pl", "--plots", type=str, default=PLOTS_FOLDER_PATH)
    parser.add_argument("-f", "--force", action='store_true', default=False)
    parser.add_argument("-ff", "--file-format", type=str, default=FILE_FORMAT)
    parser.add_argument("-fr", "--frame-rate", type=int, default=FRAME_RATE)
    args = parser.parse_args()

    if args.file_format not in SUPPORTED_FILE_EXTENSIONS:
        print(f"'{args.file_format}' file format is not supported.")
        return

    for folder_path, folder_names, file_names in os.walk(args.raw):
        for file_name in file_names:
            file_name_no_ext, file_ext = os.path.splitext(file_name)
            if not file_ext in SUPPORTED_FILE_EXTENSIONS:
                print(f"Skipped '{file_name}' as '{file_ext}' not a supported file extension.")     
                continue

            raw_file_path = os.path.join(folder_path, file_name)
            processed_file_name = f"{file_name_no_ext}.{FILE_FORMAT}"
            processed_file_path = os.path.join(args.processed, processed_file_name)
            if not args.force and os.path.exists(processed_file_path):
                print(f"Skipped '{file_name}' as already processed.")
                continue

            print(f"Processing '{file_name}'")
            raw_sample = AudioSegment.from_file(raw_file_path)
            processed_sample = process_word(raw_sample, file_name_no_ext, args.frame_rate, args.processed)
            processed_sample.export(processed_file_path, format=args.file_format)

if __name__ == "__main__":
    main()