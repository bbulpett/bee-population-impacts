import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# Import and clean data (import CSV into pandas)
df = pd.read_csv("bees.csv")
df = df.groupby(
  ['State', 'ANSI', 'Affected by', 'Year', 'state_code']
  )[
    ['Pct of Colonies Impacted']
  ].mean()

df.reset_index(inplace=True)
print(df[:5])

# App layout

