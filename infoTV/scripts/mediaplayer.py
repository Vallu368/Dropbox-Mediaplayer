import os
import subprocess
import sys
import ctypes
import time
import vlc
import pygetwindow as gw
import pyautogui
import requests
from PIL import Image, ImageTk
import pypdfium2
import dropbox
import configparser
from datetime import datetime
from configparser import ConfigParser

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))  
config_file_path = os.path.join(script_dir, 'config.ini')

# Read configuration
config = ConfigParser()
config.read(config_file_path)

APP_KEY = config.get('Dropbox', 'APP_KEY')
APP_SECRET = config.get('Dropbox', 'APP_SECRET')
REFRESH_TOKEN = config.get('Dropbox', 'REFRESH_TOKEN')
ACCESS_TOKEN = config.get('Dropbox', 'ACCESS_TOKEN')  # Initial Dropbox API key

def refresh_access_token():
    url = 'https://api.dropbox.com/oauth2/token'
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN,
        'client_id': APP_KEY,
        'client_secret': APP_SECRET,
    }

    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        response_data = response.json()
        new_access_token = response_data['access_token']
        config.set('Dropbox', 'ACCESS_TOKEN', new_access_token)
        with open(config_file_path, 'w') as configfile:
            config.write(configfile)
        print("Access token refreshed successfully!")
        return new_access_token
    else:
        print(f"Error refreshing token: {response.text}")
        return None

# Refresh access token before starting
ACCESS_TOKEN = refresh_access_token() or ACCESS_TOKEN

# Connect to Dropbox
dbx = dropbox.Dropbox(ACCESS_TOKEN)

dropbox_folder = "/InfoTV"
media_dir = os.path.join(script_dir, 'media')
print(media_dir)

if not os.path.exists(media_dir):
    os.makedirs(media_dir)

# Download files from Dropbox
def download_file(dropbox_path, local_path):
    with open(local_path, 'wb') as f:
        metadata, res = dbx.files_download(dropbox_path)
        f.write(res.content)

def download_folder(dropbox_folder, local_directory):
    if not os.path.exists(local_directory):
        os.makedirs(local_directory)
    
    result = dbx.files_list_folder(dropbox_folder)
    files_in_dropbox = {}

    while True:
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                files_in_dropbox[entry.name] = entry.path_display
            elif isinstance(entry, dropbox.files.FolderMetadata):
                new_local_folder = os.path.join(local_directory, entry.name)
                download_folder(entry.path_display, new_local_folder)

        if result.has_more:
            result = dbx.files_list_folder_continue(result.cursor)
        else:
            break

    local_files = set(os.listdir(local_directory))
    dropbox_files = set(files_in_dropbox.keys())

    for local_file in local_files:
        if local_file not in dropbox_files:
            os.remove(os.path.join(local_directory, local_file))

    for dropbox_file, dropbox_path in files_in_dropbox.items():
        local_file_path = os.path.join(local_directory, dropbox_file)
        if dropbox_file not in local_files:
            download_file(dropbox_path, local_file_path)

# Create playlist
def create_playlist(media_dir):
    download_folder(dropbox_folder, media_dir)
    playlist = []
    pdf_count = 0
    for file_name in os.listdir(media_dir):
        if file_name.lower().endswith('.pdf'):
            pdf_count += 1
            pdf = pypdfium2.PdfDocument(os.path.join(media_dir, file_name))
            for i in range(len(pdf)):
                image = pdf[i].render(scale=4).to_pil()
                image.save(f"{media_dir}/page_{i+1}_{pdf_count}.jpeg", "JPEG")
    
    for file_name in os.listdir(media_dir):
        if file_name.lower().endswith(('.mp4', '.avi', '.mkv', '.mp3', '.wav', '.jpg', '.jpeg', '.png', '.gif')):
            playlist.append(os.path.join(media_dir, file_name))
    
    return playlist

def hide_cursor():
    ctypes.windll.user32.ShowCursor(False)

def bring_vlc_to_foreground():
    possible_titles = ['VLC media player', 'VLC', 'VLC (Direct3D11 output)']
    for title in possible_titles:
        windows = gw.getWindowsWithTitle(title)
        if windows:
            vlc_window = windows[0]
            pyautogui.click(vlc_window.left + 10, vlc_window.top + 10)
            vlc_window.activate()
            time.sleep(0.5)
            vlc_window.maximize()
            hide_cursor()
            break

timer_start = time.time()
pyautogui.FAILSAFE = False
instance = vlc.Instance()
player = instance.media_player_new()
player.toggle_fullscreen()

while True:
    current_time = time.time()
    if current_time - timer_start >= 10800:  # 3 hours in seconds
        print("Refreshing Dropbox token...")
        ACCESS_TOKEN = refresh_access_token() or ACCESS_TOKEN
        dbx = dropbox.Dropbox(ACCESS_TOKEN)
        timer_start = time.time()
    
    playlist = create_playlist(media_dir)
    if not playlist:
        time.sleep(10)
        continue

    for media_file in playlist:
        if not os.path.exists(media_file):
            continue
        
        media = instance.media_new(media_file)
        player.set_media(media)
        player.play()
        time.sleep(5)
        bring_vlc_to_foreground()
        
        if media_file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            time.sleep(30)
        
        while player.is_playing():
            time.sleep(1)

    print("Playlist finished, restarting.")
