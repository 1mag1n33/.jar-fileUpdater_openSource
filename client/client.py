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
destination = data["client"]["mod-folder"]

# Send the request to the server to get the list of uploaded files
response = requests.get(server_url + '/uploads', params={'destination': destination})
if response.status_code == 200:
    uploaded_files = response.json()['files']
else:
    print(f"Error {response.status_code}: {response.reason}")
    exit(1)

# Delete files that are not in the uploads folder
for root, dirs, files in os.walk(destination):
    for file in files:
        if file not in uploaded_files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
            print(f"{file_path} has been deleted.")

print("Finished deleting files.")
