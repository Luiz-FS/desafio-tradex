from os import path, makedirs
from market import settings

def verify_process_area():
    if not path.isdir(settings.PROCESS_AREA):
        makedirs(settings.PROCESS_AREA)
