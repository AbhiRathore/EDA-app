import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime

df = pd.read_csv('uberdrive.csv')
beesdf = pd.read_csv("intro_bees.csv")
df.columns = df.columns.str.replace("*", "")
df = df[df['START_DATE'] != "Totals" ]

df['start_dt'] = df['START_DATE'].apply(lambda x : datetime.strptime(x, '%m/%d/%Y %H:%M'))
df['end_dt'] = df['END_DATE'].apply(lambda x : datetime.strptime(x, '%m/%d/%Y %H:%M'))


df['start_day'] = df['start_dt'].dt.day
df['start_hour'] = df['start_dt'].dt.hour
df['start_month'] = df['start_dt'].dt.month
df['start_month_name'] = df['start_dt'].dt.month_name()


pv = pd.pivot_table(df, index=['PURPOSE'], columns=["CATEGORY"], values=['MILES'], aggfunc=sum, fill_value=0)

trace1 = go.Bar(x=pv.index, y=pv[('MILES', 'Business')], name='Business')
trace2 = go.Bar(x=pv.index, y=pv[('MILES', 'Personal')], name='Personal')
external_stylesheets =  ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
server = app.server

df_t2 = pd.DataFrame(df.groupby(['start_month_name'])['MILES'].agg('sum'))
fig = px.line(df_t2.reset_index(), x = 'start_month_name', y = 'MILES')

fig2 = px.box(df,x = 'PURPOSE' ,y = 'MILES')

fig3 = px.choropleth(
        data_frame=beesdf,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'
    )
# ------------------------------------------------------------------------------
# App layout

app.layout = html.Div([
    html.H1('UBER drive analysis',style={'text-align': 'center'}),

    html.Div(
    children = [ 

    html.Div(
    children=[
    html.H3(children='Category-Miles',style={'text-align': 'center'}),
    html.Div(children='''Category wise analysis''',className="one-third column"),
    dcc.Graph(id='example-graph1',figure={'data': [trace1, trace2],'layout':go.Layout( barmode='stack')})

    ],className="six columns"),


    html.Div(
    children=[
    html.H3(children='Month-Miles',style={'text-align': 'center'}),
    html.Div(children='''Category wise analysis''',className="one-third column"),
    dcc.Graph(id='example-graph2',figure = fig)

    ],className="six columns"),

    ], className="row"),

    html.Div(
    children = [ 

    html.Div(
    children=[
    html.H3(children='Category-Miles',style={'text-align': 'center'}),
    html.Div(children='''Category wise analysis''',className="one-third column"),
    dcc.Graph(id='example-graph3',figure=fig2)

    ],className="six columns"),


    html.Div(
    children=[
    html.H3(children='percet of bees colonies',style={'text-align': 'center'}),
    html.Div(children='''Category wise analysis''',className="one-third column"),
    dcc.Graph(id='example-graph4',figure = fig3)

    ],className="six columns"),

    ], className="row")




])


# # ------------------------------------------------------------------------------
# # Connect the Plotly graphs with Dash Components
# @app.callback(
#     [Output(component_id='example-graph2', component_property='children')]
# )
# def update_graph():
#     df_t2 = pd.DataFrame(df.groupby(['start_month_name'])['MILES'].agg('sum'))
#     fig = px.line(df_t2.reset_index(), x = 'start_month_name', y = 'MILES')
    

#     # # Plotly Express
#     # fig = px.choropleth(
#     #     data_frame=dff,
#     #     locationmode='USA-states',
#     #     locations='state_code',
#     #     scope="usa",
#     #     color='Pct of Colonies Impacted',
#     #     hover_data=['State', 'Pct of Colonies Impacted'],
#     #     color_continuous_scale=px.colors.sequential.YlOrRd,
#     #     labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
#     #     template='plotly_dark'
#     # )

#     # Plotly Graph Objects (GO)
#     # fig = go.Figure(
#     #     data=[go.Choropleth(
#     #         locationmode='USA-states',
#     #         locations=dff['state_code'],
#     #         z=dff["Pct of Colonies Impacted"].astype(float),
#     #         colorscale='Reds',
#     #     )]
#     # )
#     #
#     # fig.update_layout(
#     #     title_text="Bees Affected by Mites in the USA",
#     #     title_xanchor="center",
#     #     title_font=dict(size=24),
#     #     title_x=0.5,
#     #     geo=dict(scope='usa'),
#     # )

#     return  fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
