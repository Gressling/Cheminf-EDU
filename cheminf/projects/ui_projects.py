# Simplified Projects UI for SQLite
from dash import dcc, html
import dash
from cheminf.app_server import server
from cheminf.db.db import execute_query

external_stylesheets = ['/static/styles.css']

app = dash.Dash(__name__,
                server=server,
                url_base_pathname="/projects/",
                title="ChemINF-EDU - Projects",
                external_stylesheets=external_stylesheets)

def get_all_projects():
    try:
        return execute_query("SELECT * FROM cheminf3_project")
    except:
        return []

app.layout = html.Div([
    html.H1("Projects Module"),
    html.P("Projects functionality temporarily simplified for SQLite migration."),
    html.P("Database connection successful!" if get_all_projects() else "Database connection failed."),
    html.A("Back to Home", href="/", style={"color": "white"})
])
