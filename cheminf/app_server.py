import os
import sys
from flask import Flask

def get_static_folder():
    """Get the static folder path, works with PyInstaller"""
    if os.environ.get('CHEMINF_STATIC_PATH'):
        # Use environment variable set by main.py for PyInstaller
        return os.environ.get('CHEMINF_STATIC_PATH')
    elif hasattr(sys, '_MEIPASS'):
        # Running as PyInstaller bundle
        return os.path.join(sys._MEIPASS, 'cheminf', 'static')
    else:
        # Running in development
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

static_folder = get_static_folder()
server = Flask(__name__, static_folder=static_folder, static_url_path='/static')