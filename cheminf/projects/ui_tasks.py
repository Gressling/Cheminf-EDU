# Simplified Tasks UI for SQLite
from dash import dcc, html
import dash
from cheminf.app_server import server
from cheminf.db.db import execute_query

external_stylesheets = ['/static/styles.css']

app = dash.Dash(__name__,
                server=server,
                url_base_pathname="/tasks/",
                title="ChemINF-EDU - Tasks",
                external_stylesheets=external_stylesheets)

def get_all_tasks():
    try:
        return execute_query("SELECT * FROM cheminf3_task")
    except:
        return []

app.layout = html.Div([
    html.H1("Tasks Module"),
    html.P("Tasks functionality temporarily simplified for SQLite migration."),
    html.P("Database connection successful!" if get_all_tasks() else "Database connection failed."),
    html.A("Back to Home", href="/", style={"color": "white"})
])
