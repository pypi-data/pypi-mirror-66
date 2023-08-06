import os
import sys
import click
from .help import BRANDING
from .utils import sys_info, error, git_configure, success, ssh_configure
from .exceptions import OsNotSupported


@click.command()
@click.version_option(message=BRANDING)
def cli():
    click.secho("Welcome to using the AzatAI Git Setup tool!", fg='blue')
    working_os = sys_info().lower()
    if working_os not in ['darwin', 'linux']:
        error(OsNotSupported)
    git_configure()
    success('Git configuring globally succeed!')
    ssh_configure(working_os)


if __name__ == '__main__':
    cli()
