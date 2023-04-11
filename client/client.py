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
response = requests.get(server_url + '/download', params={'destination': destination})
print(server_url)
print(response.content)
if response.status_code == 200:
    uploaded_files = response.json()['files']
else:
    print(f"Error {response.status_code}: {response.reason}")
    exit(1)



# Download files that are in the uploads folder but not in the destination folder
for file in uploaded_files:
    file_path = os.path.join(destination, file)
    if not os.path.exists(file_path):
        download_url = server_url + f"/downloads/{file}"
        response = requests.get(download_url)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"{file_path} has been downloaded.")
        else:
            print(f"Error {response.status_code}: {response.reason}")
    else:
        print(f"{file_path} already exists in the destination folder.")

print("Finished downloading files.")
