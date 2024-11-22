import os

DEFAULT_FRAME_RATE = 16000
DEFAULT_RAW_FOLDER_NAME = "raw"
DEFAULT_PROCESSED_FOLDER_NAME = "processed"
DEFAULT_PLOTS_FOLDER_NAME = "plots"
DEFAULT_VOICE_FOLDER_PATH = "."
DEFAULT_TARGET_FOLDER_NAME = "raw"
DEFAULT_FILE_FORMAT = "mp3"

def get_config_value(key, default_value):
    # has an environment variable been set?
    environment_variable_key = f"TEXT2SPEECH_{key}".upper()
    # is there a config file?
    # use the default
    return default_value

FRAME_RATE = get_config_value("FRAME_RATE", DEFAULT_FRAME_RATE)
RAW_FOLDER_NAME = get_config_value("RAW_FOLDER_NAME", DEFAULT_RAW_FOLDER_NAME)
PROCESSED_FOLDER_NAME = get_config_value("PROCESSED_FOLDER_NAME", DEFAULT_PROCESSED_FOLDER_NAME)
PLOTS_FOLDER_NAME = get_config_value("PLOTS_FOLDER_NAME", DEFAULT_PLOTS_FOLDER_NAME)
VOICE_FOLDER_PATH = get_config_value("VOICE_FOLDER_PATH", DEFAULT_VOICE_FOLDER_PATH)
FILE_FORMAT = get_config_value("FILE_FORMAT", DEFAULT_FILE_FORMAT)

MISSING_WORDS_FILE_NAME = "missing_words.txt"

def get_raw_folder_path(voice_folder_path: str):
    return os.path.join(voice_folder_path, RAW_FOLDER_NAME)

def get_processed_folder_path(voice_folder_path: str):
    return os.path.join(voice_folder_path, PROCESSED_FOLDER_NAME)

def get_plots_folder_path(voice_folder_path: str):
    return os.path.join(voice_folder_path, PLOTS_FOLDER_NAME)

def get_missing_words_filepath(voice_folder_path: str):
    return os.path.join(voice_folder_path, MISSING_WORDS_FILE_NAME)

SUPPORTED_FILE_EXTENSIONS = [".mp3"]