import os
from flask import Flask

static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
server = Flask(__name__, static_folder=static_folder, static_url_path='/static')