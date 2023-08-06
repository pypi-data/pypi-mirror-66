import os
from .exceptions import InvalidModeError
from pathlib import Path
import os
from pathlib import Path
import requests
import click

HOME = Path.home()
AzatAI_ROOT = os.path.join(HOME, ".AzatAI")
PROJECT_DIR = os.path.join(AzatAI_ROOT, 'addignore')
CACHE_DIR = os.path.join(PROJECT_DIR, 'cache')


def prepare_path():
    """Prepare directories for the current project"""
    # AzatAI directory ~/.AzatAI
    # Project directory ~/.AzatAI/addignore
    # Cache files directory ~/.AzatAI/addignore/cache
    for each in [AzatAI_ROOT, PROJECT_DIR, CACHE_DIR]:
        if not os.path.isdir(each):
            os.mkdir(each)


def write_to(content, destination, mode='file', force=True):
    """Write the given object or file to the destination."""
    if mode == 'file' and force:
        """Write the content to a file. The content can be a read content from python, can be a rendered content from 
        the jinja2 and so on """
        # TODO What happens if the file exists？ Have to implement when force = False
        with open(destination, 'w') as f:
            f.write(content)
    elif mode == 'object':
        """Write the object to the file, writes python pickle serialized object. the content itself should be a valid 
        python object """
        import pickle
        with open('destination', 'wb') as f:
            pickle.dump(content, f, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        raise InvalidModeError


def save_list_and_cache():
    """Get the full list available from the internet and dumps into the {now}.list.azt file.
    should save a tuple, not the list."""
    url = 'https://www.gitignore.io/api/list'
    response = get_file(url)
    return response.text


def get_result(keywords):
    url = f'https://www.gitignore.io/api/{keywords}'
    response = get_file(url)
    return response.text


def load_list_cache():
    """Loads the list cache.
    :return python tuple."""
    pass


def get_file(url):
    """Get the corresponding ignore file and cache to the ~/.AzatAI/addignore/cache/"""
    with requests.Session() as s:
        return s.get(url)


def check_cached(name):
    """Check cache status for the given file
    :return Bool True if exists, False if not"""
    pass


def print_help_msg(command):
    with click.Context(command) as ctx:
        click.echo(command.get_help(ctx))