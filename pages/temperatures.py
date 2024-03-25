import dash
from dash import dcc, html, callback, Output, Input

import os, datetime

import pandas as pd, numpy as np
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__, name = "Temperatures")







DF_TEMPERATURES = pd.read_csv(os.getcwd() + "/data/Temperatures.csv", parse_dates = True, index_col = 0)

times = []
for hour in np.arange(0, 24):
  for min in np.arange(0, 60, 10):
    times.append(datetime.time(hour, min))
  # end for min
# end for hour







layout = html.Div([    
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Temperature-Time Graph:
    
    ## Select Plots:
    html.Div([
        html.Div(
                html.Label(
                "Select Plots:", style = {"paddingTop": "20px", "color": "black"}
            ), style = {"display": "inline-block", "width": "10%"}
        ),
        html.Div(
                dcc.Dropdown(
                id="dropdown-temp-time",
                options=DF_TEMPERATURES.columns,
                value=["EFF_0.5", "EFF_1", "EFF_2", "EFF_4"],
                multi=True
            ), style = {"display": "inline-block", "width": "80%"}
        ),
    ], style = {"marginTop": "35px"}),
    
    ## Graph:
    html.Div(
        dcc.Graph(id="temp-time-graph"),
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
            html.Div(style = {"display": "inline-block", "width": "10%"}),
            html.Div(
                    html.Label(
                    "Select Date:"
                ), style = {"display": "inline-block", "width": "10%", "color": "black"}
            ),
            html.Div(
                    dcc.DatePickerSingle(
                    id = "DatePickerSingle-gradient-date",
                    min_date_allowed = DF_TEMPERATURES.index[0],
                    max_date_allowed = DF_TEMPERATURES.index[-1],
                    initial_visible_month = datetime.date(2024, 3, 1),
                    date = datetime.date(2024, 3, 1),
                    display_format = "Y-MM-DD",
                    month_format = "Y-M-D"
                ), style = {"display": "inline-block", "width": "20%"}
            ),
            html.Div(style = {"display": "inline-block", "width": "20%"}),
            ## Select Time:
            html.Div(
                html.Label(
                    "Select Time:"
                ), style = {"display": "inline-block", "width": "10%", "color": "black"}
            ),
            html.Div(
                dcc.Dropdown(
                    id="dropdown-gradient-time",
                    options=times,
                    value=datetime.time(5, 0, 0),
                    multi=False,
                ), style = {"display": "inline-block", "width": "20%"}
            ),
            html.Div(style = {"display": "inline-block", "width": "10%"}),
        ]),
        
        ## Graph:
        html.Div(
            dcc.Graph(id="temp-gradient-graph"),
            style = {"position": "absolute", "alignment": "center"}
        ),
    ], style = {"display": "inline-block", "width": "40%"}
    ),
    html.Div(style = {"display": "inline-block", "width": "30%"}),


])



##################################################################################################################
# UPDATE TEMP-TIME GRAPH:

@callback(
    Output("temp-time-graph", "figure"),
    Input("dropdown-temp-time", "value"),
)
def update_temp_time_graph(cols):
    
    df1 = DF_TEMPERATURES[cols]
    
    fig1 = px.line(df1, template = "simple_white")
    
    fig1.update_layout(
        title_x = 0.5,
        xaxis_title = "Date",
        yaxis_title = "Temperature [℃]",
        hovermode = "closest",
        autosize = True,
        font_color = "black",
        font_family = "Arial",
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

    return fig1



##################################################################################################################
# UPDATE TEMP-GRADIENT GRAPH:

@callback(
    Output("temp-gradient-graph", "figure"),
    Input("DatePickerSingle-gradient-date", "date"),
    Input("dropdown-gradient-time", "value"),
)
def update_temp_gradient_graph(date, time):
    
    datum = datetime.datetime(int(date.split("-")[0]), int(date.split("-")[1]), int(date.split("-")[2]),
                              int(time.split(":")[0]), int(time.split(":")[1]))
    
    
    y  = [100, 75, 50, 25, 0]
    
    fig2 = go.Figure()
    

    
    if datum not in DF_TEMPERATURES.index:
        plot_title = "Data not Available"
        fig2.add_trace(go.Scatter(x = [0],   y = [0], mode = "markers", name = "No Data"))
    else:
        df2 = DF_TEMPERATURES.loc[datum].to_numpy()
        plot_title = str(datum)
        fig2.add_trace(go.Scatter(x = df2[0:5],   y = y, mode = "lines+markers", name = "0.5 %"))
        fig2.add_trace(go.Scatter(x = df2[5:10],  y = y, mode = "lines+markers", name = "1.0 %"))
        fig2.add_trace(go.Scatter(x = df2[10:15], y = y, mode = "lines+markers", name = "2.0 %"))
        fig2.add_trace(go.Scatter(x = df2[15:20], y = y, mode = "lines+markers", name = "4.0 %"))
    
    
    fig2.update_layout(
        title = plot_title,
        title_x = 0.5,
        xaxis_title = "Temperature [℃]",
        yaxis_title = "Depth from bottom [mm]",
        hovermode = "closest",
        autosize = True,
        font_color = "black",
        font_family = "Arial",
        legend_title = "Reinforcement Ratio:",
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
        range = [0, 100],
    )

    return fig2



