import os

def clean_file(path):
    if os.path.exists(path):
        os.remove(path)
