import os
import click
import speech_recognition as sr

print(sr.__version__)

# get the video file

here = os.getcwd()

print(here)


@click.command()
def run():
    where = click.prompt('Enter the video file(s) directory:', type=click.Path(file_okay=False, exists=True))
    print(where)
