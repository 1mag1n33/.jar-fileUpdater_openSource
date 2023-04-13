# .jar File Updater

This is a simple Python script for updating .jar files in a directory. It communicates with a server over HTTP to retrieve a list of files to download and update.

# Getting Started

These instructions will help you set up and run the program on your local machine.

# Prerequisites

You will need the following to run the program:

Python 3.x


# Installing

Clone the repository to your local machine.
Install the requirments by running the following command in your terminal or command prompt: [pip install -r req.txt]

# Usage

Run the server by running python http_server.py in your terminal or command prompt. This will start the Flask server on port 5000.
In another terminal or command prompt window, run the client by running python client.py edit the config.yaml specifiy where u want your .jar files to be copyed to, Then run server.py in the config.yaml specifiy the location of your .jar files. This will connect to the server and update the .jar files in the upload directory in the http_server folder, Then it will download the .jar files in the specified directory.

You can customize the settings in config.yaml to change the directory to update, the URL of the server, and other settings.

# Contributing

If you'd like to contribute to the project, feel free to submit a pull request.

# License

This project is licensed under the [MIT License](LICENSE).