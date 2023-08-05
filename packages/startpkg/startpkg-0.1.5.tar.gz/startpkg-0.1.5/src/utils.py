import os.path
from pathlib import Path
import click
from datetime import datetime
import pickle
from jinja2 import Environment, PackageLoader, select_autoescape

dir_home_user = os.path.abspath(Path.home())
dir_AzatAI = os.path.join(dir_home_user, '.AzatAI')
dir_pkg = os.path.join(dir_AzatAI, 'startpkg')
path_config = os.path.join(dir_pkg, 'config.azt')


env = Environment(
    loader=PackageLoader('src', 'templates'),
)


dir_root = Path(os.path.abspath(os.path.dirname(__file__))).parent


def prepare_path_n_files():
    os.system('mkdir -p ~/.AzatAI/startpkg')


def check_file_exist(file):
    if os.path.isfile(file):
        return True
    else:
        return False


def check_dir_exist(dir):
    if os.path.isdir(dir):
        return True
    else:
        return False



def write_configure(pkg_dir,configure_object):
    with open('__version__.py','w') as f:
        f.write(configure_object)

def configure(verbose, create_data):
    config_data = {}
    if verbose:
        update_config()
    while (not check_file_exist(path_config)):
        update_config()
    with open(path_config, 'rb') as f:
        stored = pickle.load(f)

    config_data['author'] = stored['author']
    config_data['author_email'] = stored['author_email']
    config_data['license'] = stored['license']
    config_data['copyright'] = stored['copyright']

    for param in create_data.keys():
        config_data[f'{param}'] = create_data[param]

    template_version = env.get_template('__version__.py')
    return template_version.render(config_data)
    

def update_config():
    prepare_path_n_files()
    os.system('mkdir -p ~/.AzatAI/startpkg')
    config = {}
    """ Update and save the default reuseable data to the ~/.AzatAI/config.azt
    This file can be loaded when creating the new package and been used.
    """
    this_year = datetime.now().year
    config['author'] = click.prompt(
        "Package Author:", default='Yaakov Azat', confirmation_prompt=True, show_default=True)
    config['author_email'] = click.prompt(
        "Package Author Email:", default='yaakovazat@gmail.com', show_default=True)
    config['license'] = click.prompt(
        "License:", default='MIT', show_default=True)
    config['copyright'] = click.prompt(
        "Copyright:", default=f'Copyright {this_year} Azat Artificial Intelligence, LLP (AzatAI)', show_default=True)

    with open(path_config, 'wb') as f:
        pickle.dump(config, f)
