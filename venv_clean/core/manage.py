from venv_clean.core import utils


def find_virtualenvs(path='/'):
    """
    Looks up for virtual environments on a given path.
    :param path: path where to look virtual environments
    :return: list of dictionaries with virtualenv information
    """
    possible_venvs = utils.find_file('activate', path)
    venvs = []
    for e in possible_venvs :
        f = utils.get_venv_path(e)
        if not f:
            continue
        v = {}
        v['location'] = f
        v['size'] = utils.folder_size(f)
        venvs.append(v)
    return venvs
