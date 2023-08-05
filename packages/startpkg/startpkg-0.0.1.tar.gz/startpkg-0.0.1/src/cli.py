import os
from pathlib import Path
import click
from .utils import check_file_exist


def cli():
    click.secho(
        "Welcome to using the AzatAI Start Package Tool (startpkg)", fg='blue')
    print(f"preparing target files and directories:")
    os.system('pwd')
    os.system('cp -rf ./templates/* ./')
    print('Done!')