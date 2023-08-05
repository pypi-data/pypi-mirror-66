import random

from .config import load_window_names

def get_window_name(server_start, session_name, window_index):
    random.seed(server_start)

    window_names = load_window_names()

    if session_name[-1].isdigit() and int(session_name[-1]) < len(window_names) - 1:
        n = int(session_name[-1])
    else:
        n = random.randint(0, len(window_names) - 1)

    keys = list(window_names.keys())
    random.shuffle(keys)
    key = keys[n]

    window_offset = min(window_index, len(window_names[key])) - 1
    window_name = window_names[key][window_offset]

    return window_name
