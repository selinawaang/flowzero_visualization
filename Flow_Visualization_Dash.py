# Flow_Visualization_Dash
# Build a interactive data visualization of flow conditions with automated data refresh
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import geopandas as gpd
import os
import sys
import shutil

# Set Mapbox token
MAPBOX_TOKEN = "pk.eyJ1Ijoic2VsaW5hdzcyMSIsImEiOiJjbTY1ZjQ2OTkxdnp4MmxwcmN6dGNmM3ZmIn0.cEksWS0e63rPilg_CDctaw"
px.set_mapbox_access_token(MAPBOX_TOKEN)

def load_data(data_path = "../data/flow_value_viz_test/flow_value_viz_test.shp"):
    gdf = gpd.read_file(data_path)
    return gdf

external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div('Stream Gage Flow Visualization', className="text-primary text-center fs-3")
    ]),
    dbc.Row(
        dcc.Graph(figure={}, 
                  id='flow-value-map', 
                  style={'height': '800px'} )),
    dcc.Interval(
    id='interval-component',
    interval=1*1000, # in milliseconds
    n_intervals=0
    )

], fluid=True)

# Add controls to build the interaction
@callback(
    Output(component_id='flow-value-map', component_property='figure'),
    Input(component_id='interval-component', component_property='n_intervals')
)
def update_graph(n_intervals):
    df = load_data()

    fig = px.scatter_mapbox(df,
                    lat=df.geometry.y,
                    lon=df.geometry.x,
                    hover_name="sitename",
                    #animation_frame="date",
                    color = "value",
                    #color_continuous_scale='BlueScale',
                    mapbox_style = "light", 
                    opacity=0.8)
    fig.update_traces(marker=dict(size=12))
    fig.update_geos(fitbounds = "locations")

    # fig.update_geos(showland = True, landcolor = "LightGray",
    #                 showocean=True, oceancolor = "LightBlue",
    #                 showrivers = True, rivercolor = "Blue"
    #                 )
    

    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)