import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# TODO: Use plotly express to plot a bar chart instead of chloropleth
#       (x-axis is states, y-axis is bee colonies)
#       
#       Make a line chart and change dropdown to things affecting bees
#       (x-axis is years, y-axis is bee colonies, each state is different color
#       with a legend to states/colors)

app = dash.Dash(__name__)

# Import and clean data (import CSV into pandas dataframe)
df = pd.read_csv("bees.csv")
df = df.groupby(
        ['State', 'ANSI', 'Affected by', 'Year', 'state_code']
    )[
        ['Pct of Colonies Impacted']
    ].mean()  # Gets average of colonies impacted for each column

df.reset_index(inplace=True)
print(df[:5])

# App layout (Dash components and html - graphs, checkboxes, etc.)
# http://dash.plotly.com/dash-core-components
app.layout = html.Div([
    html.H1("US Bee Population Impacts", style={'text-align': 'center'}),
    dcc.Dropdown(
        id='slct_year',
        options=[
            # Year values are integers
            {"label": "2015", "value": 2015},
            {"label": "2016", "value": 2016},
            {"label": "2017", "value": 2017},
            {"label": "2018", "value": 2018},
        ],
        multi=False,
        value=2015,  # Initial value
        style={'width': '40%'}
    ),
    html.Div(id='output_container', children=[]),
    html.Br(),
    dcc.Graph(id='my_bee_map', figure={})
])

# Define callback to connect the Ployly graphs with Dash Components
@app.callback(
    [
        Output(component_id='output_container', component_property='children'),
        Output(component_id='my_bee_map', component_property='figure')
    ],
    [
        Input(component_id='slct_year', component_property='value')
    ]
)

# Each callback needs a function. Argument matches the component property.
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    # Make a copy of the dataframe
    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd]  # Defaults to default value
    dff = dff[dff["Affected by"] == "Varroa_mites"]

    # Plotly Graph Objects (go) - "old school" way
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

        # Plotly Express (px) - faster and easier
    # https://plotly.com/python-api-reference/generated/plotly.express.choropleth.html
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'
    )

    # What is returned here actually goes into the outputs of the callback
    # (arguments are POSITIONAL)
    return container, fig

# Run server
if __name__ == '__main__':
    app.run_server(debug=True)
