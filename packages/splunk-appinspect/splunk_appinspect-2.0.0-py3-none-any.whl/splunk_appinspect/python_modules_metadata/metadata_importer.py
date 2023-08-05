import os
import importlib


def import_modules(directory):
    directories_in_dir = filter(os.path.isdir, [os.path.join(directory, f) for f in os.listdir(directory)])
    # /path/to/gzip => .gzip
    sub_dir_names = ['.' + os.path.basename(d) for d in directories_in_dir]
    whitelist = [".DS_Store", ".__pycache__"]
    for subdir in sub_dir_names:
        if subdir not in whitelist:
            importlib.import_module(subdir, package='splunk_appinspect.python_modules_metadata.metadata')

def load_metadata():
    metadata_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'metadata')
    import_modules(metadata_dir)
