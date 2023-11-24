import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import dash
from dash import html, dcc, Input, Output
import plotly.express as px


# Load the data
file_path = 'athlete_events.csv'  # Replace with your file path
data = pd.read_csv(file_path)

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    # Dropdown for country selection
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': i, 'value': i} for i in data['NOC'].unique()],
        value='SWE'  # Default value set to Sweden
    ),

    # Row for graphs
    html.Div([
        # Column for the first graph
        html.Div([
            dcc.Graph(id='top-sports-graph')
        ], style={'width': '50%', 'display': 'inline-block'}),

        # Column for the second graph
        html.Div([
            dcc.Graph(id='gender-dist-graph')
        ], style={'width': '50%', 'display': 'inline-block'})
    ]),
    # Row for additional graphs
    html.Div([
    # Column for the average age graph
    html.Div([
        dcc.Graph(id='avg-age-graph')
    ], style={'width': '50%', 'display': 'inline-block'}),

    # Column for the average height/weight graph
    html.Div([
        dcc.Graph(id='avg-height-weight-graph')
    ], style={'width': '50%', 'display': 'inline-block'})
])
])

# Callback for updating top-sports-graph
@app.callback(
    Output('top-sports-graph', 'figure'),
    Input('country-dropdown', 'value'))
def update_top_sports_graph(selected_country):
    # Handle the case where no country is selected initially
    if selected_country is None:
        return px.bar()

    # Filter data for the selected country and where medals were won
    filtered_data = data[(data['NOC'] == selected_country) & data['Medal'].notna()]

    # Count medals won per sport
    medals_per_sport = filtered_data.groupby('Sport')['Medal'].count().sort_values(ascending=False).head(10)

    # Create the bar graph
    fig = px.bar(medals_per_sport, x=medals_per_sport.values, y=medals_per_sport.index, 
                 labels={'x': 'Number of Medals', 'y': 'Sport'}, orientation='h')
    fig.update_layout(title_text=f'Medals Won in Top 10 Sports in {selected_country}')
    return fig

# Callback for updating gender-dist-graph
@app.callback(
    Output('gender-dist-graph', 'figure'),
    Input('country-dropdown', 'value'))
def update_gender_dist_graph(selected_country):
    filtered_data = data[data['NOC'] == selected_country]
    gender_distribution = filtered_data['Sex'].value_counts().reset_index()
    gender_distribution.columns = ['Gender', 'Count']
    fig = px.pie(gender_distribution, values='Count', names='Gender')
    fig.update_layout(title_text=f'Gender Distribution in {selected_country}')
    return fig
#Callback for avg age
@app.callback(
    Output('avg-age-graph', 'figure'),
    Input('country-dropdown', 'value'))
def update_avg_age_graph(selected_country):
    filtered_data = data[data['NOC'] == selected_country]
    avg_age = filtered_data['Age'].mean()

    # Create a bar graph for average age
    fig = px.bar(x=['Average Age'], y=[avg_age], labels={'x': '', 'y': 'Age'})
    fig.update_layout(title_text=f'Average Age of Athletes in {selected_country}')
    return fig
#Callback for average height/weight
@app.callback(
    Output('avg-height-weight-graph', 'figure'),
    Input('country-dropdown', 'value'))
def update_avg_height_weight_graph(selected_country):
    filtered_data = data[data['NOC'] == selected_country]
    avg_height = filtered_data['Height'].mean()
    avg_weight = filtered_data['Weight'].mean()

    # Create a bar graph for average height and weight
    fig = px.bar(x=['Average Height', 'Average Weight'], y=[avg_height, avg_weight],
                 labels={'x': '', 'y': 'Value'})
    fig.update_layout(title_text=f'Average Height and Weight of Athletes in {selected_country}')
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
