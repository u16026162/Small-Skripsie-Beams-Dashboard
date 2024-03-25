import dash
from dash import dcc, html, callback, Output, Input

import os, datetime

import pandas as pd, numpy as np
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__, name = "Solar Radiation")





DF_SOLAR = pd.read_csv(os.getcwd() + "/data/Solar_Radiation.csv", parse_dates = True, index_col = 0)


##################################################################################################################
# UPDATE SOLAR-TIME GRAPH:
    
fig1 = px.line(DF_SOLAR, template = "simple_white")

fig1.update_layout(
    title_x = 0.5,
    xaxis_title = "Date",
    yaxis_title = "Solar Radiation [m<sup>2</sup>]",
    hovermode = "closest",
    autosize = True,
    font_color = "black",
    font_family = "Arial",
    showlegend = False,
    legend_title = None
)
fig1.update_xaxes(
    title_font_family = "Arial Black",
    showgrid = True,
    gridcolor = "gray",
    mirror = True,
)
fig1.update_yaxes(
    title_font_family = "Arial Black",
    showgrid = True,
    gridcolor = "gray",
    mirror = True,
)





##################################################################################################################
# LAYOUT:


layout = html.Div([
    

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## Graph:
    html.Div(
        dcc.Graph(id="solar-time-graph", figure = fig1), 
        style = {"width": "98%", "height": "98%"}
    ),
    
    ## Line
    html.Hr(
        style = {"height": "2px", "color": "black", "border": "none", "backgroundColor": "black"}
    ),
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Temperature-Gradient Graph:
    
    html.Div(style = {"display": "inline-block", "width": "30%"}),
    html.Div([
        html.Div([
            ## Pick Date:
            html.Div(style = {"display": "inline-block", "width": "30%"}),
            html.Div(
                    html.Label(
                    "Select Date:"
                ), style = {"display": "inline-block", "width": "20%", "color": "black"}
            ),
            html.Div(
                    dcc.DatePickerSingle(
                    id = "DatePickerSingle-solar-date",
                    min_date_allowed = DF_SOLAR.index[0],
                    max_date_allowed = DF_SOLAR.index[-1],
                    initial_visible_month = datetime.date(2024, 3, 2),
                    date = datetime.date(2024, 3, 2),
                    display_format = "Y-MM-DD",
                    month_format = "Y-M-D"
                ), style = {"display": "inline-block", "width": "20%"}
            ),
            html.Div(style = {"display": "inline-block", "width": "30%"}),
        ]),
        
        ## Graph:
        html.Div(
            dcc.Graph(id="solar-daily-graph"),
            style = {"position": "absolute", "alignment": "center"}
        ),
        
    ], style = {"display": "inline-block", "width": "40%"}
    ),
    html.Div(style = {"display": "inline-block", "width": "30%"}),
    
])





##################################################################################################################
# UPDATE SOLAR-DAILY GRAPH:

@callback(
    Output("solar-daily-graph", "figure"),
    Input("DatePickerSingle-solar-date", "date"),
)
def update_daily_solar_graph(date):
    
    datum_start = datetime.datetime(int(date.split("-")[0]), int(date.split("-")[1]), int(date.split("-")[2]))
    datum_end   = datetime.datetime(int(date.split("-")[0]), int(date.split("-")[1]), int(date.split("-")[2])+1)
    
    
    if datum_start not in DF_SOLAR.index:
        plot_title = "Data not Available"
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x = [0],   y = [0], mode = "markers", name = "No Data"))
    else:
        df2 = DF_SOLAR.loc[datum_start:datum_end]
        plot_title = str(date)
        fig2 = px.line(df2, template = "simple_white")
    
    
    fig2.update_layout(
        title = plot_title,
        title_x = 0.5,
        xaxis_title = "Time",
        yaxis_title = "Solar Radiation [m<sup>2</sup>]",
        hovermode = "closest",
        autosize = True,
        font_color = "black",
        font_family = "Arial",
        showlegend = False,
        legend_title = None,
        width = 650,
        height = 600,
        template = "simple_white",
    )
    fig2.update_xaxes(
        title_font_family = "Arial Black",
        showgrid = True,
        gridcolor = "gray",
        mirror = True,
    )
    fig2.update_yaxes(
        title_font_family = "Arial Black",
        showgrid = True,
        gridcolor = "gray",
        mirror = True,
    )

    return fig2



