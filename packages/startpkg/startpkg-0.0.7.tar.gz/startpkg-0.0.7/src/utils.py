import os.path
from pathlib import Path


dir_root = Path(os.path.abspath(os.path.dirname(__file__))).parent


def check_file_exist(file):
    if os.path.isfile(os.path.join(dir_root, file)):
        return True
    else:
        return False
