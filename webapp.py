import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dash_table
from dash.dependencies import Input, Output

import pandas as pd
from sqlalchemy import create_engine

from pathlib import Path

import plotly.graph_objects as go
import plotly.express as px

import flask

# Where is our database, wherever we're running this?
# and let's abstract with SQLAlchemy
scriptPath = Path(__file__).parent
dbPath = scriptPath / 'db'
dbPathFile = str(dbPath / 'db_cryptocompare.sqlite')
db_uri = r'sqlite:///' + str(dbPathFile)

# Connect to our db from SQLAlchemy
# playing safe, making these global
global db, df, groups
db = create_engine(db_uri)

# App's raw data
#sql = 'Select [symbol],[close],[time] From Value_ByMinute_BTC'
# We want latest 15 prices but sorted ascending
sql = 'Select [symbol],[time],[close] From ' \
    '(select * from Value_ByMinute_BTC ' \
     'ORDER BY [time] DESC limit 15) ORDER BY [symbol],[Time] ASC;'
df= pd.read_sql(sql,db)
# From that, create unique Managers for Drop Down
groups = sorted(df['symbol'].unique())

# Create our DASH app object!
#app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
# THIS IS FOR GUNICORN (in production server) TO HOOK INTO!
#server = app.server

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#server = flask.Flask(__name__) # define flask app.server
app = dash.Dash(__name__, external_stylesheets=external_stylesheets) # , server=server call flask server
server = app.server

# On server, will run in command in something like
#gunicorn webapp:app.server -b 0.0.0.0 #:8000
# to make run
# sudo systemctl start gunicorn...



#
# Part 1: DATA FUNCTIONS
#
#
#  Groups of data for our dropdown, which drives table and chart
def data_group_options_build():
    OptionList = [{'label': group, 'value': group} for group in groups]
    return OptionList
#
#  Fill DATATABLE from Dropdown List
def data_table_populat(dropdown_value):
    is_group = df['symbol']==dropdown_value
    # Create dataframe of those rows only by passing in those booleans
    dff = df[is_group] # dff as in dataframe filtered
    # Data table won't work without column defs
    my_table_columns = [{"name": i, "id": i,} for i in (df.columns)]
    
    return dff.to_dict('records'), my_table_columns
    
#
# Draw GRAPH from data picked in manager dropdown list
def data_graph_draw(dropdown_value):
    is_group = df['symbol']==dropdown_value
    # Create dataframe of those rows only by passing in those booleans
    dff = df[is_group] # dff as in dataframe filtered
    # Using HELPER library plotly.express as px
    fig = px.scatter(dff, x=dff['time'], y=dff.close)
    return fig

##### END DATA FUNCTIONS #####
#
# STYLES
#
# Give style same names as DASH uses, purpose here to keep app.layout ucluttered
#
style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left',
            'width': '200px'
        } for c in ['close','time']
        ] + [
        {
            'if': {'column_id': 'symbol'},
            'display': 'none'
        } 
        ] + [
        {
            'if': {'column_id': 'close'},
            'textAlign': 'right',
            'width': '200px'
        } 
        ] + [
        {
            'if': {'column_id': 'time'},
            'width': '200px'
        } 
        ]
style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ]
style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
    }

#
# PART 2, Create our clean DASH LAYOUT object
#
app.layout = html.Div([
    html.H1(children='Python automation charts using cryptocurrencies'),
        # dumm y callback to get things initialized
        dcc.Input(id='initialize_app_components_with_dummy_callback', value='', type='text', style={'display':'none'}),
        # html.Div to keep Dropdown and 'Data Table' text on same line
        html.Div([dcc.Dropdown(id='group-dropdown', value='BTC', style={'width': '100px', 'verticalAlign':'middle'}),
        html.H3(children=' Table Data', style={'verticalAlign':'middle','display': 'inline-block'})
        ]),
        
    html.Br(),
    dash_table.DataTable(id='table-container',
        style_table = {'width':'500px'},
        style_cell_conditional = style_cell_conditional,
        style_data_conditional = style_data_conditional,
        style_header = style_header),
    html.H3(children='Cryptocurrenty Prices by Minute'),
    dcc.Graph(id='graph-container')
])
#
# PART 2, Load Initial DROPDOWN LIST DATA in our DASH layout which
# will happen after the app is run.
#
@app.callback(
    Output(component_id='group-dropdown', component_property='options'),
    [Input(component_id='initialize_app_components_with_dummy_callback', component_property='value')]
)
def group_dropdown_BuildOptions(df_for_dropdown):  
    return data_group_options_build()
#
# PART 3, set up our callbacks to hands dropdown selections, etc
#

#
# Callback: TABLE POPULATE based on drop down selection
#
@app.callback([Output('table-container', 'data'), Output('table-container', 'columns')],
    [Input('group-dropdown', 'value')])
def gen_table(dropdown_value):
    return data_table_populat(dropdown_value)
    
#
# Callback: GRAPH DRAW based on drop down selection
#  
@app.callback(
    dash.dependencies.Output('graph-container', 'figure'),
    [dash.dependencies.Input('group-dropdown', 'value')])
def gen_graph(dropdown_value):
    return data_graph_draw(dropdown_value)

###
### OKAY, LET 'ER RIP
###    

if __name__ == '__main__':
    # Can this ever work instead of dummy callback?
    #app.callback(Output('mgr-dropdown', 'options')) (mgr_options_build())
    
    app.run_server(debug=True)
