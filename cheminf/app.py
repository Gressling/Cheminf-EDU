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

# Polished start page template with grouped navigation sections.
START_PAGE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>ChemINF-EDU Start Page</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
  </head>
  <body>
    <header>
      <h1>ChemINF-EDU</h1>
    </header>
    <div class="container">
      <nav>
        <div class="nav-section">
          <h2>Programs</h2>
          <ul>
            <li><a href="/molecules/">Molecules</a></li>
            <li><a href="/inventory/">Inventory</a></li>
          </ul>
        </div>
        <div class="nav-section">
          <h2>REST Resources</h2>
          <ul>
            <li><a href="/api/molecules">REST API: Molecules Data (JSON)</a></li>
            <li><a href="/api/inventory">REST API: Inventory Data (JSON)</a></li>
            <li><a href="/static/REST_documentation.html">REST API Documentation</a></li>
          </ul>
        </div>
      </nav>
      <div class="card">
        <h2>Welcome to ChemINF-EDU!</h2>
        <p>Select one of the options above to start exploring our cheminformatics platform.</p>
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