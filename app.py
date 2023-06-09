import os
import json
import dash
from dash import Dash,dcc,Output,Input
import dash_bootstrap_components as dbc
import dash_deck
import dash_html_components as html
import pydeck as pdk
import pandas as pd
import plotly.express as px
import pathlib  #just for deploy on server when reading csv from local

PATH = pathlib.Path(__file__).parent  #just for deploy on server when reading csv from local
DATA_PATH = PATH.joinpath("data").resolve()  #just for deploy on server when reading csv from local
df=pd.read_csv(DATA_PATH.joinpath("TBRPM_SE_ALL.csv"))  #just for deploy on server when reading csv from local

#df = pd.read_csv('TBRPM_SE_ALL.csv')
## df_POP = pd.read_csv('data/TBRPM_SE_ALL.csv',
##                    dtype = {"ZONE": str})
## df_POP['POPEMP']=df_POP['POP']+df_POP['EMP']
## print(df_POP)

geoJSONFile = DATA_PATH.joinpath("TBRPM_TAZ_WGS84_Project.geojson")  #just for deploy on server when reading csv from local
#geoJSONFile = 'data/TBRPM_TAZ_WGS84_Project.geojson'
with open(geoJSONFile) as response:
    polygons = json.load(response)





#build dash components (every dash app has components that are displayed on the page through layout which interact with eachother through the call back )

app=Dash(__name__,external_stylesheets=[dbc.themes.LUX])
server=app.server
mytitle=dcc.Markdown(children='')
mygraph=dcc.Graph(figure={})
dropdown=dcc.Dropdown(options=df.columns.values[6:8],
                      value='DU',
                      clearable='False')

#customize your own layout
app.layout=dbc.Container([
    dbc.Row([
        dbc.Col([mytitle],width=6)
    ],justify='center'),
    dbc.Row([
        dbc.Col([mygraph],width=12),
    ]),
    dbc.Row([
        dbc.Col([dropdown],width=6)
    ],justify='center')
    
],fluid=True)


#callback allows components to interact
@app.callback(
    Output(mygraph,component_property='figure'),
    Output(mytitle,component_property='children'),
    Input(dropdown,component_property='value')
)
def update_graph(column_name):
    print(column_name)
    print(type(column_name))
    fig = px.choropleth_mapbox(
    data_frame = df,            # Data frame with values
    geojson = polygons,                      # Geojson with geometries
    featureidkey = 'properties.TAZ2015', # Geojson key which relates the file with the data from the data frame
    locations = 'ZONE',               # Name of the column of the data frame that matches featureidkey
    color = column_name,                # Name of the column of the data frame with the data to be represented
    color_continuous_scale="Viridis",
    mapbox_style = 'open-street-map',
    center = dict(lat = 28.3, lon = -82),
    opacity=0.8,
    animation_frame='YEAR',
    labels={"ZONE":"ZONE# ","POPEMP": "TOTAL SE DATA"})
    fig.update_layout(autosize=False,width=1400,height=750)
    #fig.update_geos(fitbounds="locations", visible=True)
    return fig, '# '+column_name

#Run app
if __name__=='__main__':
    app.run_server(debug=FALSE)
