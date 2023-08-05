import os
from pathlib import Path
import pickle
import click
from .utils import check_file_exist, configure, write_configure

dir_home_user = os.path.abspath(Path.home())
dir_AzatAI = os.path.join(dir_home_user, '.AzatAI')
dir_pkg = os.path.join(dir_AzatAI, 'startpkg')
path_config = os.path.join(dir_pkg, 'config.azt')


@click.command()
@click.option('-v', '--verbose', help='Regenerate the copyright base(Author and email information for further packages.)', default=False, show_default=True)
def cli(verbose):
    """AzatAI Start Package Tool (startpkg) CLI"""
    click.secho(
        "Welcome to using the AzatAI Start Package Tool (startpkg)", fg='blue')
    create_data = {}
    click.secho('Input package information below:\n', fg='blue')
    create_data['pkg_name'] = click.prompt('Package Name:')
    create_data['pkg_description'] = click.prompt('Package Description:')
    create_data['pkg_url'] = click.prompt('Package URL:')
    create_data['pkg_version'] = click.prompt('Package Version(x.y.z):')

    here = os.path.abspath(os.path.dirname(__file__))
    pkg_path = os.path.join(here, create_data['pkg_name'])
    cmd_dir = f"mkdir ./{pkg_path}"
    pkg_content = [
        '__init__.py',
        '__cli.py__',
        'exceptions.py',
        'help.py',
        'models.py',
        'status_codes.py',
        'utils.py'
    ]
    for each in pkg_content:
        file_path = os.path.join(pkg_path, f'{each}')
        cmd_touch = f'touch {file_path}'
        os.system(cmd_touch)
    pkg_root = {
        'dirs':[
            'tests',
        ],
        'files':[
            'README.md',
            'LICENSE',
            'MANIFEST.in',
            '.travis.yml',
            'requirements.txt',
        ]
    }
    for each in pkg_root['files']:
        Path.touch(os.path.join(here, f'{each}'), exist_ok=True)
    for each in pkg_root['dirs']:
        if not os.path.isdir(os.path.join(here,f'{each}')):
            os.makedirs(os.path.join(here, f'{each}'), exist_ok=True)
    rendered = configure(verbose, create_data)
    write_configure(pkg_path,rendered)

