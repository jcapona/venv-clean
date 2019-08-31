import re
import os


def folder_size(path):
    """
    Calculates the size of a folder
    :param path: path to folder to analyze
    :return: size in MB of the folder
    """
    size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.isfile(fp) and not os.path.islink(fp):
                size += os.path.getsize(fp)
    return round(size / (1024.0 * 1024.0), 2)


def find_file(name, path):
    """
    Finds files with the given name on a certain path
    :param name: filename to lookup
    :param path: path where file will be searched
    :return: array of strings with absolute paths
    """
    arr = []
    path = os.path.abspath(path)
    for root, dirs, files in os.walk(path):
        if name in files:
            p = os.path.join(root, name)
            arr.append(p)
    return arr


def get_venv_path(path):
    """
    Goes through the 'activate' virtualenv script to find the
    VIRTUAL_ENV line and validate that the folder is actually a
    virtual environment
    :param path: path to the 'activate' script
    :return: boolean indicating virtualenv status
    """
    if not os.path.isfile(path):
        return None, None

    prefix = 'VIRTUAL_ENV='
    regex = '^' + prefix + '(.)+'
    pattern = re.compile(regex)

    r = None
    for i, line in enumerate(open(path)):
        for match in re.finditer(pattern, line):
            r = eval(match.group().split(prefix)[-1])
            break
        if r: break

    return r
