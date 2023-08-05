#!/usr/bin/env python3
__author__ = "Azat Artificial Intelligence, LLP (AzatAI)"
__copyright__ = "Copyright 2020, AzatAI"
__credits__ = ["Yaakov Azat", ]
__license__ = "MIT"
__version__ = "0.0.0"
__maintainer__ = "Yaakov Azat"
__email__ = "yaakovazat@gmail.com"
__status__ = "Development"

"""

                                                                                                                                    
                                                                                                                                    
               AAA                                                          tttt                        AAA               IIIIIIIIII
              A:::A                                                      ttt:::t                       A:::A              I::::::::I
             A:::::A                                                     t:::::t                      A:::::A             I::::::::I
            A:::::::A                                                    t:::::t                     A:::::::A            II::::::II
           A:::::::::A           zzzzzzzzzzzzzzzzz  aaaaaaaaaaaaa  ttttttt:::::ttttttt              A:::::::::A             I::::I  
          A:::::A:::::A          z:::::::::::::::z  a::::::::::::a t:::::::::::::::::t             A:::::A:::::A            I::::I  
         A:::::A A:::::A         z::::::::::::::z   aaaaaaaaa:::::at:::::::::::::::::t            A:::::A A:::::A           I::::I  
        A:::::A   A:::::A        zzzzzzzz::::::z             a::::atttttt:::::::tttttt           A:::::A   A:::::A          I::::I  
       A:::::A     A:::::A             z::::::z       aaaaaaa:::::a      t:::::t                A:::::A     A:::::A         I::::I  
      A:::::AAAAAAAAA:::::A           z::::::z      aa::::::::::::a      t:::::t               A:::::AAAAAAAAA:::::A        I::::I  
     A:::::::::::::::::::::A         z::::::z      a::::aaaa::::::a      t:::::t              A:::::::::::::::::::::A       I::::I  
    A:::::AAAAAAAAAAAAA:::::A       z::::::z      a::::a    a:::::a      t:::::t    tttttt   A:::::AAAAAAAAAAAAA:::::A      I::::I  
   A:::::A             A:::::A     z::::::zzzzzzzza::::a    a:::::a      t::::::tttt:::::t  A:::::A             A:::::A   II::::::II
  A:::::A               A:::::A   z::::::::::::::za:::::aaaa::::::a      tt::::::::::::::t A:::::A               A:::::A  I::::::::I
 A:::::A                 A:::::A z:::::::::::::::z a::::::::::aa:::a       tt:::::::::::ttA:::::A                 A:::::A I::::::::I
AAAAAAA                   AAAAAAAzzzzzzzzzzzzzzzzz  aaaaaaaaaa  aaaa         ttttttttttt AAAAAAA                   AAAAAAAIIIIIIIIII
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                                                                                          
"""
import os
import sys
import click


def cli():
    """Example script."""
    click.echo('Hello World!')
    click.secho("Welcome to using the AzatAI Git Setup tool!", fg='blue')
    git_install()
    git_configure()
    ssh_configure()
    click.secho('Done!',bg='blue')



def git_install():
    click.echo("Install or update git")
    os.system('sudo apt update && sudo apt install git')


def git_configure():
    click.echo("Configuring git globally")
    # backup the original one
    os.system('cp ~/.gitconfig ~/.gitconfig.backup')

    git_user_name = click.prompt('Please input your name:', type=str)
    git_user_mail = click.prompt('Please input your email address:', type=str)

    if click.confirm(f"These are your credentials, are they true?\n {git_user_mail}\n{git_user_name}"):
        cmd_name = f'git config --global user.name "{git_user_name}"'
        cmd_mail = f'git config --global user.mail "{git_user_mail}"'
        os.system(cmd_name)
        os.system(cmd_mail)
    cmd_name = f'git config --global user.name "{git_user_name}"'
    cmd_mail = f'git config --global user.mail "{git_user_mail}"'
    os.system(cmd_name)
    os.system(cmd_mail)

def copy_and_show_ssh():
    # add to agent
    # copy to clipboard
    # show at the console
    # start the ssh agent in the background
    os.system('eval "$(ssh-agent -s)"')
    os.system('ssh-add ~/.ssh/id_rsa')
    click.echo(
        'We need to install xclip to copy data to the clipboard,you will be asked to enter ur password:')
    os.system('sudo apt-get install xclip')
    os.system('xclip -sel clip < ~/.ssh/id_rsa.pub')
    click.echo('Copies the contents of the id_rsa.pub file to your clipboard succeeded, if not you can also copy the contents below manually:')
    os.system('clear')
    os.system('cat ~/.ssh/id_rsa.pub')
    click.echo(
        'Now open github.com and your github settings, paste the copied content(or contents above) to the new SSH key!')


def ssh_configure():
    # check installed ?
    if os.path.isfile('~/.ssh/id_rsa.pub'):
        copy_and_show_ssh()
    else:
        # create new else
        click.echo("No valid ssh key found! Generating a new one: (Type enter to continue)")
        os.system("ssh-keygen -t rsa -b 4096 -N ''")
        copy_and_show_ssh()



if __name__ == "__main__":
    cli()