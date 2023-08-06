import os
import sys
import click
from .help import BRANDING
from pathlib import Path
import speech_recognition as sr

sr_path = os.path.dirname(sr.__file__)
data_path = os.path.join(sr_path, 'pocketsphinx-data')


@click.command()
@click.version_option(message=BRANDING)
def cli():
    """'AzatAI v2t tool : Extracts text from the video, This is not a subtitle extraction tool, this tool uses ASR to
    extract text from the video files."""
    click.secho('AzatAI video to text Automation tool')
    where = click.prompt('Enter the video file(s) directory:', type=click.Path(file_okay=False, exists=True))
    all_files = [Path(x) for x in os.listdir(where)]
    videos = [x for x in all_files if x.suffix in ['.mp4', 'mpeg', 'avi', 'mp3']]
    here = os.getcwd()
    click.secho(f'Working on {os.getcwd()}', fg='yellow')

    if not os.path.isdir(data_path):
        os.chdir(sr_path)
        click.secho(f'Working on {os.getcwd()}', fg='yellow')
        cmd = f"git clone https://github.com/AzatAI/pocketsphinx-data"
        os.system(cmd)

    os.chdir(here)
    click.secho(f'Working on {os.getcwd()}', fg='yellow')
    os.chdir(where)
    click.secho(f'Working on {os.getcwd()}', fg='yellow')
    for each in videos:
        cmd = f"ffmpeg -i {each} {each}.wav"
        click.secho(cmd, fg='yellow')
        os.system(cmd)
        click.secho('Generated Audio File Successfully', fg='green')
        click.secho(f'{sr.__version__}')
        r = sr.Recognizer()
        audio_file = sr.AudioFile(f'{each}.wav')
        with audio_file as source:
            audio = r.record(source)
        click.echo(r.recognize_sphinx(audio, language='zh-CN'))
    os.chdir(here)
    click.secho(f'Working on {os.getcwd()}', fg='yellow')


if __name__ == '__main__':
    cli()

# Please try the following steps
#
# git clone --recursive https://github.com/bambocher/pocketsphinx-python
# cd pocketsphinx-python
# Edit file pocketsphinx-python/deps/sphinxbase/src/libsphinxad/ad_openal.c
# Change
# #include <al.h>
# #include <alc.h>
#
# to
#
# #include <OpenAL/al.h>
# #include <OpenAL/alc.h>
#
# python setup.py install
