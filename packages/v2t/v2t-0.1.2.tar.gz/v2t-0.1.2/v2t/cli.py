import click


@click.command()
@click.version_option()
def cli():
    """'AzatAI v2t tool : Extracts text from the video, This is not a subtitle extraction tool, this tool uses ASR to
    extract text from the video files.
    Usage: v2t [options] <video_source_dir target_text_path> (OR <video_url>)"""
    # TODO
    #  Download video from BiliBili Automatically. option -b --bilibili bilibili video url.
    #  Auto process v2t
    #  Get Youtube video subtitles (both auto generated and mannual added) option -y --youtube youtube video url
    #  OCR hardcore video subtitles.  option -o  --ocr  give video location and destination.
    click.echo('Welcome to use AzatAI tools!')
