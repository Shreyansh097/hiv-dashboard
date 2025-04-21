import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load data
df = pd.read_csv("unicef_indicator_1.csv")

# Clean 'obs_value' (handle values like '<100')
df["obs_value_clean"] = df["obs_value"].replace(r"[<>\s]", "", regex=True).replace('', None).astype(float)

# Initialize the app
app = dash.Dash(__name__)
app.title = "UNICEF HIV Infections Dashboard"

# App layout
app.layout = html.Div([
    html.H1("Estimated New HIV Infections (UNICEF)"),
    
    html.Label("Select Country:"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': c, 'value': c} for c in df['country'].unique()],
        value='India'
    ),
    
    html.Label("Select Sex:"),
    dcc.Dropdown(
        id='sex-dropdown',
        options=[{'label': s, 'value': s} for s in df['sex'].unique()],
        value='Female'
    ),

    html.Label("Select Age Group:"),
    dcc.Dropdown(
        id='age-dropdown',
        options=[{'label': a, 'value': a} for a in df['current_age'].unique()],
        value='10 to 19 years old'
    ),

    dcc.Graph(id='trend-graph')
])

# Callback
@app.callback(
    Output('trend-graph', 'figure'),
    Input('country-dropdown', 'value'),
    Input('sex-dropdown', 'value'),
    Input('age-dropdown', 'value')
)
def update_graph(country, sex, age):
    filtered = df[(df['country'] == country) & 
                  (df['sex'] == sex) & 
                  (df['current_age'] == age)]

    fig = px.line(filtered, x='time_period', y='obs_value_clean',
                  title=f"New HIV Infections in {country}",
                  labels={'time_period': 'Year', 'obs_value_clean': 'Estimated Infections'})
    fig.update_layout(transition_duration=500)
    return fig

# Run server
if __name__ == '__main__':
    app.run_server(debug=True)
