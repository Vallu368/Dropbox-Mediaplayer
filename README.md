# Dropbox-Mediaplayer
Program to create an infoscreen using Python, VLC and Dropbox

#Requirements
VLC Mediaplayer
Python
Dropbox folder called "InfoTV"

#Usage
Create a Dropbox account, then go to Dropbox.com/developers, and create an app
Open the config.ini, and input your Dropbox apps details
You can get the initial access token (last for 4 hours), the app_key and app_secret from your apps developer console.
To get the refresh_key, follow Dropbox's tutorials here: https://developers.dropbox.com/oauth-guide
once you have all of them in your config.ini, all you need to do is put some media you wish to play in the "InfoTV" folder on your Dropbox account, and launch the "infotv" bat file from the root folder

#How it works
The bat file creates another bat file in your shell:startup to make the program automatially launch when the computer is launched, delete that if you don't want it!
The program looks for media in your Dropbox folder, then downloads it, and plays it. If something is deleted from the Dropbox folder, it will delete it from your local folder too, once the last playlist it has created has been played.
