import PyInstaller.__main__

PyInstaller.__main__.run([
    'updater_server.py',                 # path to your Python script
    '--onefile',                 # create a single-file executable
    '--name=updater_server',             # name of the executable
    '--icon=my_icon.ico',        # path to the application icon (optional)
])
