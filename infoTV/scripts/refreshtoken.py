import os
import requests
from configparser import ConfigParser

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))  

# Full path to the config file
config_file_path = os.path.join(script_dir, 'config.ini')

# Read configuration from the full path of config.ini
config = ConfigParser()  # Use the correct import here
config.read(config_file_path)

APP_KEY = config.get('Dropbox', 'APP_KEY')
APP_SECRET = config.get('Dropbox', 'APP_SECRET')
REFRESH_TOKEN = config.get('Dropbox', 'REFRESH_TOKEN')

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
        # If the request is successful, you'll receive a new access token
        response_data = response.json()
        new_access_token = response_data['access_token']
        
        # Save the new access token back to your config file
        config.set('Dropbox', 'ACCESS_TOKEN', new_access_token)
        with open(config_file_path, 'w') as configfile:  # Use the full path here
            config.write(configfile)
        
        print("Access token refreshed successfully!")
        return new_access_token
    else:
        print(f"Error refreshing token: {response.text}")
        return None

# Call the function to refresh the token and update the config file
new_token = refresh_access_token()

if new_token:
    print("NEW TOKEN")
    print(new_token)
else:
    print("Failed to refresh the token.")
