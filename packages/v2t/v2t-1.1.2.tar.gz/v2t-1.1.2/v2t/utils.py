import os
import click
import speech_recognition as sr

print(sr.__version__)


def check_and_fix_pocketsphinx():
    try:
        import pocketshpinx
    except ModuleNotFoundError:
        clone_cmd = 'git clone --recursive https://github.com/AzatAI/pocketsphinx-pytho'
        os.system(clone_cmd)
        click.secho('Cloned sphinx-python to current folder.')



def check_and_fix_sphinx_data():
    """Check user installed or not the chinese language pack, if not then download and install"""

