from flask import Flask, render_template_string, url_for, request, redirect, session
from dash import Dash, html

from cheminf.molecules.rest_api import server as api_server
from cheminf.molecules.ui import app as dash_app
from cheminf.app_server import server
import os
# Import dash apps so that they register with the shared server.
import cheminf.molecules.ui         # molecules dash app
import cheminf.inventory.ui         # inventory dash app
import cheminf.projects.ui_projects # projects maintenance dash app
import cheminf.projects.ui_tasks    # tasks maintenance dash app
import cheminf.projects.rest_api    # REST API endpoints for projects/tasks
import cheminf.molecules.rest_api   # REST API endpoints for molecules
import cheminf.inventory.rest_api   # REST API endpoints for inventory
import cheminf.reactions.rest_api   # Register Reactions REST endpoints
import cheminf.reactions.ui_reactions # (If you create a UI for reactions)
import cheminf.reactions.ui_reactionparticipants  # For reaction participants UI
import cheminf.reactions.ui_overview  # Reaction Overview UI page

# --- NEW: Import LIMS experiments modules ---
import cheminf.lims_experiments.rest_api      # REST API endpoints for LIMS experiments
import cheminf.lims_experiments.ui_experiments  # LIMS experiments UI page
import cheminf.lims_experiments.ui_samples      # LIMS samples UI page
import cheminf.lims_experiments.ui_measurements # LIMS measurements UI page

# --- Import Time Series modules ---
import cheminf.time_series.rest_api           # REST API endpoints for time series
import cheminf.time_series.ui_timeseries      # Time Series analysis UI page

# Load configuration from settings.json
from cheminf.config import INSTANCE_NAME
server.secret_key = 'dev_secret_key_change_in_production'  # Should be in settings.json for production
instance_name = INSTANCE_NAME

# --- Basic Login/Logout Implementation for UI only ---

@server.before_request
def require_login():
    # Allow REST API endpoints and static files without login
    if request.path.startswith('/api') or request.path.startswith('/static'):
        return None
    # Allow access to login and logout pages
    if request.path in ['/login', '/logout']:
        return None
    # If not authenticated, redirect to login
    if not session.get('authenticated'):
        return redirect(url_for('login'))

@server.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        from cheminf.config import ADMIN_USERNAME, ADMIN_PASSWORD
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password.'
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>Login - ChemINF-EDU {{ instance_name }}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
      </head>
      <body>
        <header><h1>ChemINF-EDU</h1></header>
        <div class="container">
          <div class="card">
            <h2>Please Log In to {{ instance_name }} system</h2>
            {% if error %}
              <p style="color:red;">{{ error }}</p>
            {% endif %}
            <form method="post">
              <div>
                <label>Username:</label>
                <input type="text" name="username" required>
              </div>
              <div>
                <label>Password:</label>
                <input type="password" name="password" required>
              </div>
              <div>
                <button type="submit">Login</button>
              </div>
            </form>
          </div>
        </div>
      </body>
    </html>
    """, error=error, instance_name=instance_name)

@server.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))

# --- End Basic Login/Logout Implementation ---

# Home route with descriptive text
@server.route('/home')
def home():
    home_content = """
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>Welcome to ChemINF-EDU</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 20px; color: #eee }
          h2 { color: #eee; }
          ul { margin-top: 10px; }
          ul li { margin-bottom: 5px; }
        </style>
      </head>
      <body>
        <h2>Welcome to ChemINF-EDU</h2>
        <p>
          ChemINF-EDU is a comprehensive cheminformatics system designed to support a wide range of chemical data management tasks.
          It combines powerful user interfaces with robust RESTful APIs to provide seamless integration across various modules.
        </p>
        <p>This platform offers the following modules:</p>
        <ul>
          <li><strong>Molecules:</strong> Manage and view detailed information about chemical molecules.</li>
          <li><strong>Inventory:</strong> Track and manage chemical inventory data including amounts and storage details.</li>
          <li><strong>Projects Maintenance:</strong> Organize and monitor projects related to chemical research and analysis.</li>
          <li><strong>Tasks Maintenance:</strong> Manage individual tasks and workflows within larger projects.</li>
          <li><strong>Reactions Maintenance:</strong> Define, view, and update chemical reaction data and kinetics.</li>
          <li><strong>Reaction Participants Maintenance:</strong> Oversee reaction components including reactants, products, and catalysts with their respective stoichiometric details.</li>
          <li><strong>Reaction Overview:</strong> Generate comprehensive overviews and chemical equations from aggregated reaction data.</li>
          <li><strong>LIMS Experiments:</strong> Access experiment, sample, and measurement data.</li>
          <li><strong>REST API:</strong> Leverage a suite of RESTful endpoints for easy integration, automation, and data sharing across various applications.</li>
        </ul>
        <p>
          Use the navigation menu on the left to learn more about each module and start interacting with the platform.
        </p>
      </body>
    </html>
    """
    return home_content

# Updated start page template using an iframe to load pages on the right
START_PAGE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>ChemINF-EDU @{{ instance_name }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      body {
        margin: 0;
        font-family: Arial, sans-serif;
        color: #fff; /* white font on startpage */
        background: #111; /* dark background for whole app */
      }
      .header {
        background: #333;
        color: white;
        padding: 10px 20px;
      }
      .header h1 {
        margin: 0;
        display: inline-block;
      }
      .header a {
        color: white;
        text-decoration: none;
        float: right;
        margin-top: 5px;
        padding: 5px 10px;
        border: 2px solid white;
        border-radius: 4px;
        transition: all 0.3s ease;
      }
      .header a:hover {
        color: #00aced;
      }
      .container {
        width: 130%; /* 30% wider overall */
        margin: 0 auto; /* center container */
        display: flex;
        height: calc(100vh - 60px);
      }
      .nav {
        width: 250px;
        background: #222; /* dark background */
        padding: 20px;
        box-sizing: border-box;
        overflow-y: auto;
        border-right: 1px solid #444;
      }
      .nav h2 {
        margin-top: 0;
        color: #fff;
      }
      .nav ul {
        list-style: none;
        padding: 0;
      }
      .nav li {
        margin: 10px 0;
      }
      .nav li a {
        text-decoration: none;
        color: #fff;
        display: block;
        padding: 6px 8px;
      }
      .nav li a:hover {
        color: #00aced;
      }
      .content {
        flex-grow: 1;
      }
      .content iframe {
        width: 100%;
        height: 100%;
        border: none;
      }
      /* Additional styling for nav footer */
      .nav .footer {
        margin-top: 20px;
        border-top: 1px solid #444;
        padding-top: 10px;
      }
    </style>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
  </head>
  <body>
    <div class="header">
      <h1>ChemINF-EDU</h1>
      <a href="{{ url_for('logout') }}" target="_self">Logout</a>
    </div>
    <div class="container">
      <div class="nav">
        <!-- Top navigation link for Home -->
        <ul>
          <li><a href="/home" target="mainFrame">Home</a></li>
          <li><a href="/projects/" target="mainFrame">Projects Maintenance</a></li>
          <li><a href="/tasks/" target="mainFrame">Tasks Maintenance</a></li>
        </ul>
        <h2>ELN</h2>
        <ul>
          <li><a href="/experiments/" target="mainFrame">Experiments</a></li>
          <li><a href="/molecules/" target="mainFrame">Molecules</a></li>
          <li><a href="/inventory/" target="mainFrame">Inventory</a></li>
          <li><a href="/reactions/" target="mainFrame">Reactions Maintenance (old)</a></li>
          <li><a href="/reactions/participants/" target="mainFrame">Reaction Participants Maintenance (old)</a></li>
          <li><a href="/reactions/overview/" target="mainFrame">Reaction Overview (old)</a></li>
        </ul>
        <h2>LIMS</h2>
        <ul>
          <li><a href="/samples/" target="mainFrame">Samples</a></li>
          <li><a href="/measurements/" target="mainFrame">Measurements</a></li>
        </ul>
        <h2>Time Series Analysis</h2>
        <ul>
          <li><a href="/timeseries/" target="mainFrame">Time Series Charts</a></li>
        </ul>
        <h2>REST Resources</h2>
        <ul>
          <li><a href="/api/molecules" target="mainFrame">REST API: Molecules Data (JSON)</a></li>
          <li><a href="/api/inventory" target="mainFrame">REST API: Inventory Data (JSON)</a></li>
          <li><a href="/api/projects" target="mainFrame">Projects API (JSON)</a></li>
          <li><a href="/api/reactions" target="mainFrame">REST API: Reactions Data (old) (JSON)</a></li>
          <li><a href="/api/v1/timeseries/experiments" target="mainFrame">REST API: Time Series Experiments (JSON)</a></li>
          <li><a href="/static/REST_documentation.html" target="mainFrame">REST API Documentation</a></li>
        </ul>
        <!-- Footer navigation with Logout -->
        <div class="footer">
          <ul>
            <li><a href="{{ url_for('logout') }}" target="_self">Logout</a></li>
          </ul>
        </div>
      </div>
      <div class="content">
        <iframe name="mainFrame" src="/home"></iframe>
      </div>
    </div>
  </body>
</html>
"""

@server.route('/')
def index():
    return render_template_string(START_PAGE, instance_name=instance_name)

if __name__ == '__main__':
    server.run(debug=True, port=8050)