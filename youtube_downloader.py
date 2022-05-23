import os
import PySimpleGUI as gui
from pytube import YouTube

def restart_progress_bar():
    window['-PROGRESSBAR-'].update(0)

def on_progress(stream, chunk, remaining_bytes):
    progress = 100 - round(remaining_bytes / stream.filesize * 100)
    window['-PROGRESSBAR-'].update(progress)

def on_complete(stream, file_path):
    pass

layout = [
    [gui.Text('URL:'), gui.Input(key = '-URL-', expand_x = True), gui.Button('Search', key = 'search')], # URL Input + search button
    [gui.Text('Title: '), gui.Text('', key = '-TITLE-')], # Video title
    [gui.Text('Length: '), gui.Text('', key = '-LENGTH-')], # Length in minutes
    [gui.Text('Audio size: '), gui.Text('', key = '-SIZE-')], # Size in MB
    [gui.Text('Download directory: '), gui.Input(key = '-OUTPUTPATH-'), gui.FolderBrowse()],
    [gui.Button('Download', key = 'download'), gui.Progress(100, size = (20, 20), expand_x = True, key = '-PROGRESSBAR-')] # download button + progress bar
]

window = gui.Window('YouTube Downloader', layout)

while True:
    event, values = window.read()

    if event == gui.WIN_CLOSED:
        break

    if event == 'search':
        restart_progress_bar()
        if not values['-URL-']:
            continue
        youtube_video_info = YouTube(values['-URL-'], on_progress_callback = on_progress, on_complete_callback = on_complete)
        window['-TITLE-'].update(youtube_video_info.title)
        window['-LENGTH-'].update(f'{round(youtube_video_info.length / 60, 2) } minutes')
        window['-SIZE-'].update(f'{round(youtube_video_info.streams.get_audio_only().filesize / 1048576, 1) } MB')

    if event == 'download':
        restart_progress_bar()
        downloaded_audio_file = youtube_video_info.streams.get_audio_only().download(output_path = values['-OUTPUTPATH-'])
        base, ext = os.path.splitext(downloaded_audio_file)
        os.rename(downloaded_audio_file, base + '.mp3')

window.close()
