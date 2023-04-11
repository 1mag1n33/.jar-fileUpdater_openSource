from flask import Flask, request, jsonify
from src.yaml_template import template
import os
import yaml
import glob
import shutil

app = Flask(__name__)

CONFIG_FILE = 'config.yaml'

if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'w') as file:
        yaml.dump(template, file)

with open(CONFIG_FILE, 'r') as file:
    data = yaml.safe_load(file)

# Create the uploads directory if it doesn't exist
if not os.path.exists('uploads'):
    os.mkdir('uploads')

@app.route('/upload', methods=['POST'])
def upload():
    # Check if the file is in the request
    if 'file' not in request.files:
        return jsonify({'message': 'No file provided'}), 400

    file = request.files['file']
    print(file)
    filename = file.filename

    # Save the file to the server
    file.save(os.path.join('uploads', filename))

    return jsonify({'message': 'File uploaded successfully'}), 200

@app.route('/download', methods=['GET'])
def download():
    # Get the destination folder from the request
    destination = request.args.get('destination')
    if not destination:
        return jsonify({'message': 'No destination provided'}), 400

    # Replace backslashes with forward slashes in the destination path
    destination = destination.replace('\\', '/')

    # Copy all files in the uploads folder to the destination folder
    for file_path in glob.glob('uploads/*'):
        file_name = os.path.basename(file_path)
        destination_path = os.path.join(destination, file_name)
        shutil.copy(file_path, destination_path)

    return jsonify({'message': 'Files downloaded successfully'}), 200

@app.route('/delete', methods=['DELETE'])
def delete():
    # Get the filename from the request
    filename = request.args.get('filename')
    if not filename:
        return jsonify({'message': 'No filename provided'}), 400

    # Remove the file from the uploads directory
    file_path = os.path.join('uploads', filename)
    try:
        os.remove(file_path)
    except OSError as e:
        return jsonify({'message': f'Failed to delete file: {str(e)}'}), 500

    return jsonify({'message': 'File deleted successfully'}), 200


if __name__ == '__main__':
    app.run(port=data["server"]["port"])
