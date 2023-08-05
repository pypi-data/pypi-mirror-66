"""A utility library to facitlitate installation testing."""

# Python Standard Libraries
import shutil
import platform
import six
# Third-Party Libraries
# N/A
# Custom Libraries
# N/A


def copy_directory(source_path, destination_path):
    """Helper function to address short-comings of the shutil.copyTree method.

    See: https://stackoverflow.com/questions/1303413/python-shutil-copytree-ignore-permissions

    Arguments:
        source_path (String): The path to the directory to copy from
        destination_path (String): The path to the directory to copy to

    Returns:
        None
    """
    if platform.system() == "Windows":
        if six.PY3:
            magic_prefix = "\\\\?\\"
        else:
            # TODO make deep path on windows compatible in python2.7
            magic_prefix = ""
    else:
        magic_prefix = ''

    _orig_copystat = shutil.copystat

    if six.PY2:
        shutil.copystat = lambda x, y: x
    else:

        def copystat(src, dst, follow_symlinks=True, *args):
            return src

        shutil.copystat = copystat

    shutil.copytree(magic_prefix + source_path, magic_prefix + destination_path, symlinks=True)
    shutil.copystat = _orig_copystat
