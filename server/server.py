import requests
import os
import time
import yaml
from src.yaml_template import template
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

CONFIG_FILE = 'config.yaml'

if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'w') as file:
        yaml.dump(template, file)
    
else:
    with open(CONFIG_FILE, 'r') as file:
        data = yaml.safe_load(file)


class ModHandler(FileSystemEventHandler):
    def __init__(self, server_url, mod_dir):
        self.server_url = server_url
        self.processed_files = set()
        self.mod_dir = mod_dir

    def send_to_server(self, file_path):
        print(f"Sending file to server: {file_path}")
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(self.server_url, files=files)
        if response.status_code == 200:
            self.processed_files.add(file_path)
            print(f"File sent successfully: {file_path}")
        else:
            print(f"Failed to send file: {file_path}")

    def on_created(self, event):
        if event.is_directory:
            return None
        elif event.src_path.endswith(".jar"):
            print(f"New mod file created: {event.src_path}")
            self.send_to_server(event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return None
        elif event.src_path.endswith(".jar") and event.src_path not in self.processed_files:
            print(f"Mod file modified: {event.src_path}")
            self.send_to_server(event.src_path)

    def process_all_files(self):
        for file_name in os.listdir(self.mod_dir):
            if file_name.endswith(".jar") and file_name not in self.processed_files:
                file_path = os.path.join(self.mod_dir, file_name)
                self.send_to_server(file_path)


if __name__ == "__main__":
    mod_dir = data["server"]["path_to_jars"]
    server_url = f"{data['server']['url']}/upload"
    event_handler = ModHandler(server_url, mod_dir)
    event_handler.process_all_files()
    observer = Observer()
    observer.schedule(event_handler, mod_dir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
