from setuptools import setup

APP = ['BengtClip.py']  # Your main entry file
DATA_FILES = ['resources/BengtClip_white.icns']
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'resources/BengtClip_white.icns', 
    'packages': ['rumps', 'pyperclip'],
    'plist': {
        'LSUIElement': True  # Hides the Dock icon and app window, only shows in menubar
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)