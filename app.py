
import dash
import dash_html_components as html
import dash_core_components as dcc

import pandas as pd
import re,sys,os
import numpy as np
import plotly.graph_objs as go
import plotly.express as px ## 4.4.1

from scipy.stats import zscore

from time import time  # To time our operations
from collections import defaultdict  # For word frequency
datapath = os.getcwd()
# fix random seed for reproducibility
np.random.seed(7)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

revDF=pd.read_csv(datapath + '/zomato.csv')
total_Rest_type = list(set(revDF['rest_type'].unique()))
total_Rest_type_clean = []

for rtype in total_Rest_type:
    if pd.isna(rtype) != True:
        for each in [f.strip() for f in rtype.strip().split(",")]:
            #print(each)
            total_Rest_type_clean.append(each)

total_Rest_type_clean = list(set(total_Rest_type_clean))

g = []
for k in total_Rest_type_clean:
    tdf= {}
    tdf['label'] = k
    tdf['value'] = k
    g.append(tdf)



totalcuisines = list(set(revDF['cuisines'].unique()))
totalcuisines_clean = []

for ctype in totalcuisines:
    if pd.isna(ctype) != True:
        for each in [f.strip() for f in ctype.strip().split(",")]:
            #print(each)
            totalcuisines_clean.append(each)
totalcuisines_clean = list(set(totalcuisines_clean))

cuisinelist = []
for k in totalcuisines_clean:
    tdf= {}
    tdf['label'] = k
    tdf['value'] = k
    cuisinelist.append(tdf)


cuisinelist2 = []
for k in totalcuisines_clean + ['All']:
    tdf= {}
    tdf['label'] = k
    tdf['value'] = k
    cuisinelist2.append(tdf)


## location list 

total_locations = list(set(revDF['location'].unique()))
total_locations_clean = []

for ltype in total_locations:
    if pd.isna(ltype) != True:
        total_locations_clean.append(ltype)
total_locations_clean = list(set(total_locations_clean))


loclist = []
for k in total_locations_clean + ['All']:
    tdf= {}
    tdf['label'] = k
    tdf['value'] = k
    loclist.append(tdf)


def ratingfinder(s):
    if pd.isna(s) != True:
        return s.split("/")[0]
    else:
        return s
    
def ratecleaner(x):
    try:
        x = re.sub("[^0-9\.]",'',x)
        return float(x)
    except:
        #print(x)
        return 0
        
   





app.layout = html.Div([
    html.H1('Bangalore Restaurant analysis',style={'text-align': 'center'}),

    html.Div(
    children = [ 

   


    html.Div(
    children=[
    #html.H3(children='Drop down',style={'text-align': 'center'}),
    html.Div(children='''Select Restaurant type''',className="one-third column"),
    dcc.Dropdown(
            id='my_dropdown',
            options=g,
            value=total_Rest_type_clean[0],
            multi=False,
            clearable=False,
            style={"width": "50%","color": "black"}
        ),

    ],className="six columns"),


    
    html.Div(
    children=[
    #html.H3(children='Drop down',style={'text-align': 'center'}),
    html.Div(children='''Select cuisine type''',className="one-third column"),
    dcc.Dropdown(
            id='my_dropdown_cuisine',
            options=cuisinelist,
            value=totalcuisines_clean[0],
            multi=False,
            clearable=False,
            style={"width": "50%","color": "black"}
        ),

    ],className="six columns"),




    ], className="row"),


    html.Div(
    children = [ 

    html.Div(
    children=[
    html.H3(children='Types of Restaurants',style={'text-align': 'center'}),
    html.Div(children='''Category wise analysis''',className="one-third column"),
    dcc.Graph(id='the_graph2',style={"color": "black"})

    ],className="six columns"),


    html.Div(
    children=[
    html.H3(children='Types of cuisines available',style={'text-align': 'center'}),
    html.Div(children='''Category wise analysis''',className="one-third column"),
    dcc.Graph(id='the_graph3',style={"color": "black"})

    ],className="six columns"),

    ], className="row"),



    html.Div(
    children = [

    html.Div(
    children=[
    #html.H3(children='Drop down',style={'text-align': 'center'}),
    html.Div(children='''Select locations ''',className="one-third column"),
    dcc.Dropdown(
            id='loc_dropdown',
            options=loclist,
            value=total_locations_clean[0],
            multi=False,
            clearable=False,
            style={"width": "50%","color": "black"}),

    ],className="five columns"),


    html.Div(
    children=[
    html.Div(children='''Select cuisine ''',className="one-third column"),
    dcc.Dropdown(
            id='cusin_dropdown',
            options=cuisinelist2,
            value=totalcuisines_clean[0],
            multi=False,
            clearable=False,
            style={"width": "50%","color": "black"}),

    ],className="five columns"),

    ]),



    
    html.Div(
        children = [ 

        html.Div(
        children=[
        html.H3(children='cost vs ratings of restaurants',style={'text-align': 'center'}),
        html.Div(children='''cost vs ratings of restaurants'''),
        dcc.Graph(id='the_graph4',style={"color": "black"})

        ],className="twelve columns"),



        ], className="row"),




],style={"color": "white", 'background-color': 'black'})












@app.callback(
    dash.dependencies.Output('the_graph2', 'figure'),
    [dash.dependencies.Input('my_dropdown', 'value')])

def update_output(value):
        
    temdintype = revDF[revDF['rest_type'].str.contains(value,na=False)]
    w=temdintype.location.value_counts(normalize = True)*100
    w = w.reset_index()
    w.columns = ['location','number of restaurants']

    fig = px.pie(w, values='number of restaurants', names='location', 
                title='location wise number of restaurants for {}'.format(value),
                template='plotly_dark')
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig


    

@app.callback(
    dash.dependencies.Output('the_graph3', 'figure'),
    [dash.dependencies.Input('my_dropdown_cuisine', 'value')])

def update_output(value):
        
    temdintype = revDF[revDF['cuisines'].str.contains(value,na=False)]
    w=temdintype.location.value_counts(normalize = True)*100
    w = w.reset_index()
    w.columns = ['location','number of restaurants']

    fig = px.pie(w, values='number of restaurants', names='location', 
                title='location wise number of restaurants for {}'.format(value),
                template='plotly_dark')
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig



@app.callback(
    dash.dependencies.Output('the_graph4', 'figure'),
    [dash.dependencies.Input('loc_dropdown', 'value'),
    dash.dependencies.Input('cusin_dropdown', 'value')])

def update_output(location,cusvalue):
    print('lvalue is {}'.format(location))
    print('value is {}'.format(cusvalue))
        
        
    revDF['rate2'] = revDF['rate'].apply(lambda x : ratingfinder(x))
    

    revDF2 = revDF[(pd.notna(revDF['rate2'])) & ~(revDF['rate2'].isin(['NEW']))]
    revDF2['ratings'] = revDF2['rate2'].apply(lambda x : ratecleaner(x))

    #print(revDF2)

    tdf_loc = revDF2[revDF2['location'].str.contains(location,na=False)]
    

    if cusvalue != "All":
        tdf_loc_cusine = tdf_loc[tdf_loc['cuisines'].str.contains(cusvalue,na=False)]
    elif cusvalue == "All":
         tdf_loc_cusine = tdf_loc

    #print(tdf_loc_cusine)



    fig =fig = px.scatter(tdf_loc_cusine, x="ratings", y="approx_cost(for two people)", size="votes", color = "rest_type",
           hover_name="name",size_max=50,title='cost vs rating for {}'.format(cusvalue),
                template='plotly_dark')


    return fig








if __name__ == '__main__':
    app.run_server(debug=True)
