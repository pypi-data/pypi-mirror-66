
import click
import pyperclip
import subprocess
from time import sleep
import shlex


@click.command()
@click.option('--clipboard', is_flag=True)
@click.option('--selection', is_flag=True)
def main(clipboard, selection):

    """
        Get text from selection or clipboard and open it in Google Chrome
        E.g URL: https://google.com
        E.g URL: https://stackoverflow.com
    """
    
    if selection:
        url_from_clipboard = subprocess.check_output((shlex.split('xclip -out -selection')))
        subprocess.call(['google-chrome', '--new-window', url_from_clipboard])
    elif clipboard:
        url_from_clipboard = pyperclip.paste()
        subprocess.call(['google-chrome', '--new-window', url_from_clipboard])
    else:
        click.echo('Missing option: --clipboard or --selection')
    
