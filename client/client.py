import os
import yaml
import requests
from src.yaml_template import template

CONFIG_FILE = 'config.yaml'

if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'w') as file:
        yaml.dump(template, file)

with open(CONFIG_FILE, 'r') as file:
    data = yaml.safe_load(file)

server_url = data["client"]["url"]

# Set the destination folder to the user's mod folder
destination = data["client"]["mod-folder"].replace('\\', '/')

# Send the request to the server
response = requests.get(server_url, params={'destination': destination})
print(response.text)

# Print the server's response
print(response.json()['message'])
