from flask import Flask, render_template_string, url_for, request, redirect, session
from dash import Dash, html

from cheminf.molecules.rest_api import server as api_server
from cheminf.molecules.ui import app as dash_app
from cheminf.app_server import server
import os
from dotenv import load_dotenv
# Import dash apps so that they register with the shared server.
import cheminf.molecules.ui  # molecules dash app
import cheminf.inventory.ui  # inventory dash app
import cheminf.molecules.rest_api  # REST API endpoints
import cheminf.inventory.rest_api  # register inventory API endpoints

# Load environment variables
load_dotenv()
server.secret_key = os.getenv('SECRET_KEY')
instance_name = os.getenv('INSTANCE')

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
        # Use hard-coded credentials; adjust as needed
        load_dotenv()
        if username == os.getenv('ADMIN_USERNAME') and password == os.getenv('ADMIN_PASSWORD'):
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
        <header>
          <h1>ChemINF-EDU</h1>
        </header>
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

# Polished start page template with grouped navigation sections.
START_PAGE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>ChemINF-EDU @{{ instance_name }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
  </head>
  <body>
    <header>
      <h1>ChemINF-EDU</h1>
      <a href="{{ url_for('logout') }}" style="float:right; margin:10px; color:white;">Logout</a>
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
        <h2>Welcome to Cheminf-EDU ({{ instance_name }})</h2>
        <p>Select one of the options above to start exploring our cheminformatics platform.</p>
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