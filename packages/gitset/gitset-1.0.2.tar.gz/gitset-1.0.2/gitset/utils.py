import os
import click
import platform


def sys_info():
    """Check the current operating system, return either darwin or linux or windows."""
    return platform.system()


def validate_path(path):
    """Validate a path"""
    return os.path.isdir(path)


def error(msg):
    return click.secho(msg, fg='red')


def info(msg):
    return click.secho(msg, fg='blue')


def success(msg):
    return click.secho(msg, fg='green')


def git_configure():
    click.echo("Configuring git globally")
    # backup the original one
    os.system('cp ~/.gitconfig ~/.gitconfig.backup')

    git_user_name = click.prompt('Please input your name:', type=str)
    git_user_mail = click.prompt('Please input your email address:', type=str)
    cmd_name = f'git config --global user.name "{git_user_name}"'
    cmd_mail = f'git config --global user.mail "{git_user_mail}"'
    os.system(cmd_name)
    os.system(cmd_mail)


def copy_and_show_ssh(operating_system):
    # add to ssh agent
    # copy to clipboard
    # show at the console
    # start the ssh agent in the background
    os.system('eval "$(ssh-agent -s)"')
    os.system('ssh-add ~/.ssh/id_rsa')
    if operating_system == 'linux':
        """Install xclip for linux operating systems"""
        click.echo(
            'We need to install xclip to copy data to the clipboard,you will be asked to enter ur password:')
        os.system('sudo apt-get install xclip')
        os.system('xclip -sel clip < ~/.ssh/id_rsa.pub')
    elif operating_system == 'darwin':
        os.system('pbcopy < ~/.ssh/id_rsa.pub')
    click.echo(
        'Copies the contents of the id_rsa.pub file to your clipboard succeeded, if not you can also copy the '
        'contents below manually:')
    os.system('clear')
    os.system('cat ~/.ssh/id_rsa.pub')
    click.echo(
        'Now open github.com and your github settings, paste the copied content(or contents above) to the new SSH key!')


def ssh_configure(operating_system):
    # check installed ?
    if os.path.isfile('~/.ssh/id_rsa.pub'):
        copy_and_show_ssh(operating_system)
    else:
        # create new else
        click.echo("No valid ssh key found! Generating a new one: (Type enter to continue)")
        os.system("ssh-keygen -t rsa -b 4096 -N ''")
        copy_and_show_ssh(operating_system)
