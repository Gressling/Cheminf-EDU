# filepath: /c:/htdocs/non-github/Cheminf-EDU/src/main.py
from flask import Flask, render_template_string, url_for
from dash import Dash, html

from cheminf.molecules.rest_api import server as api_server
from cheminf.molecules.ui import app as dash_app
from cheminf.app_server import server
# Import dash apps so that they register with the shared server.
import cheminf.molecules.ui  # molecules dash app
import cheminf.inventory.ui  # inventory dash app
import cheminf.molecules.rest_api  # REST API endpoints
import cheminf.inventory.rest_api  # register inventory API endpoints

# Define a simple start page template.
START_PAGE = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>ChemINF-EDU Start Page</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
    <meta name="viewport" content="width=device-width, initial-scale=1">
  </head>
  <body>
    <div class="container">
      <h1>Welcome to ChemINF-EDU</h1>
      <nav>
        <ul>
          <li><a href="/molecules/">Molecules</a></li>
          <li><a href="/inventory/">Inventory</a></li>
          <li><a href="/api/molecules">REST API: Molecules Data (JSON)</a></li>
          <li><a href="/api/inventory">REST API: Inventory Data (JSON)</a></li>
        </ul>
      </nav>
      <div class="card">
        <p>Select one of the above options to continue.</p>
      </div>
    </div>
  </body>
</html>
"""

@server.route('/')
def index():
    return render_template_string(START_PAGE)

if __name__ == '__main__':
    server.run(debug=True, port=8050)