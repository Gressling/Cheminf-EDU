from dash import dcc, html, Input, Output, exceptions
import dash
from cheminf.app_server import server
from cheminf.db.db import get_db_connection
from cheminf.config import DB_NAME, DB_PREFIX

app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname="/reactions/overview/",
    title="ChemINF-EDU - Reaction Overview",
    external_stylesheets=['/static/styles.css']
)

app.layout = html.Div([
    # Home link in header
    html.Div(
      html.A("Home", href="/", style={"color": "white", "textDecoration": "none"}),
      style={"textAlign": "right", "padding": "10px"}
    ),
    html.H1("Reaction Overview"),
    html.Button("Load Reaction Overview", id="load-overview-btn"),
    html.Div(id="overview-result", style={"marginTop": "20px", "padding": "10px", "border": "1px solid #ccc"})
])

@app.callback(
    Output("overview-result", "children"),
    Input("load-overview-btn", "n_clicks")
)
def load_overview(n_clicks):
    if not n_clicks:
        raise exceptions.PreventUpdate
    # Execute the overview query for ReactionID=1
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = f"""
    SELECT 
      r.ReactionName,
      r.ReactionDescription,
      CONCAT(
        'Reactants: ', GROUP_CONCAT(CASE WHEN rp.Role = 'reactant' 
                                          THEN CONCAT(rp.StoichiometricCoefficient, ' ', m.MoleculeUpacName, ' (', m.SMILES, ')')
                                          END SEPARATOR ' + '),
        ' | Products: ', GROUP_CONCAT(CASE WHEN rp.Role = 'product' 
                                          THEN CONCAT(rp.StoichiometricCoefficient, ' ', m.MoleculeUpacName, ' (', m.SMILES, ')')
                                          END SEPARATOR ' + '),
        ' | Catalysts: ', GROUP_CONCAT(CASE WHEN rp.Role = 'catalyst' 
                                          THEN CONCAT(rp.StoichiometricCoefficient, ' ', m.MoleculeUpacName, ' (', m.SMILES, ')')
                                          END SEPARATOR ', ')
      ) AS ReactionEquation
    FROM {DB_NAME}.{DB_PREFIX}reactions r
    JOIN {DB_NAME}.{DB_PREFIX}reactionparticipants rp ON r.ReactionID = rp.ReactionID
    JOIN {DB_NAME}.{DB_PREFIX}molecules m ON rp.MoleculeID = m.id
    WHERE r.ReactionID = %s
    GROUP BY r.ReactionID, r.ReactionName, r.ReactionDescription;
    """
    cursor.execute(query, (1,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return html.Div([
            html.H3(result["ReactionName"]),
            html.P(result["ReactionDescription"]),
            html.P(result["ReactionEquation"], style={"fontWeight": "bold"})
        ])
    else:
        return html.P("No reaction data found.")

if __name__ == '__main__':
    app.run_server(debug=True)