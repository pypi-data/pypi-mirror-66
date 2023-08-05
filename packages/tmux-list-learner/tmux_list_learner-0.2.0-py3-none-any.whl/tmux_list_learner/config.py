import yaml
import random
from collections import OrderedDict
import os
from enum import Enum
import appdirs

APPNAME='tmux-list-learner'
APPAUTHOR='flaxandteal'

class ListOrder(Enum):
    ASIS = 0
    RANDOM = 1
    ALPHA = 2

def get_default_window_lists():
    return [
            {'name': 'network-top', 'order': ListOrder.ASIS.name, 'items': ['Application', 'Presentation', 'Session', 'Transport', 'Network', 'Data-Link', 'Physical']},
            {'name': 'trad-major-rivers-africa', 'order': ListOrder.ASIS.name, 'items': ['Nile', 'Niger', 'Senegal', 'Congo', 'Orange', 'Limpopo', 'Zambezi']},
            {'name': 'wonders-of-ancient-world', 'order': ListOrder.ALPHA.name, 'items': ['Pyramid-Giza', 'Gardens-Babylon', 'Zeus-Olympia', 'Artemis-Ephesus', 'Mausoleum-Halicarnassus', 'Colossus-Rhodes', 'Lighthouse-Alexandria']}
    ]

def load_window_names(overwrite=False):
    appdir = appdirs.user_config_dir(APPNAME, APPAUTHOR)
    os.makedirs(appdir, exist_ok=True)

    list_path = os.path.join(appdir, 'list.yaml')
    if overwrite or not os.path.exists(list_path):
        with open(list_path, 'w') as list_yaml:
            yaml.dump(get_default_window_lists(), list_yaml)

    with open(list_path, 'r') as list_yaml:
        window_lists = yaml.load(list_yaml, Loader=yaml.SafeLoader)

    for window_list in window_lists:
        if 'order' in window_list:
            window_list['order'] = ListOrder[window_list['order']]
            if window_list['order'] is ListOrder.ALPHA:
                window_list['items'] = sorted(window_list['items'])
            elif window_list['order'] is ListOrder.RANDOM:
                random.shuffle(window_list['items'])

    window_names = OrderedDict([(i['name'], i['items']) for i in window_lists])

    return window_names
