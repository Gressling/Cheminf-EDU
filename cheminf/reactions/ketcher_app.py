import dash
from dash import html
import dash_bootstrap_components as dbc

# Load Ketcher JS and CSS from the CDN (latest version)
external_scripts = [
    "https://unpkg.com/@epam/ketcher@latest/dist/ketcher.js"
]
external_stylesheets = [
    "https://unpkg.com/@epam/ketcher@latest/dist/ketcher.css",
    dbc.themes.BOOTSTRAP  # Optional: for basic styling
]

app = dash.Dash(__name__,
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Ketcher Reaction Editor"),
    # The container where Ketcher will be initialized.
    html.Div(id="ketcher-container", style={"height": "600px", "border": "1px solid #ccc"}),
    # Example button to interact with Ketcher (e.g., get reaction data)
    html.Button("Get Reaction", id="get-reaction-btn"),
    html.Pre(id="reaction-output"),
    # Inline script to initialize Ketcher after the DOM loads.
    html.Script("""
        document.addEventListener("DOMContentLoaded", function() {
            if (typeof Ketcher === "undefined") {
                console.error("Ketcher library is not loaded.");
                return;
            }
            // Create a new Ketcher instance inside the container.
            // You can pass additional configuration options if needed.
            window.ketcherInstance = new Ketcher(document.getElementById("ketcher-container"), {});
        });
    """, type="text/javascript")
])

if __name__ == '__main__':
    app.run_server(debug=True)
