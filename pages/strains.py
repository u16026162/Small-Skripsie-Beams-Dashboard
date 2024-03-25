import dash
from dash import dcc, html, callback, Output, Input

import os, datetime

import pandas as pd, numpy as np
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__, name = "Strains")



DF_STRAINS = pd.read_csv(os.getcwd() + "/data/Strains.csv", parse_dates = True, index_col = 0)

times = []
for hour in np.arange(0, 24):
  for min in np.arange(0, 60, 10):
    times.append(datetime.time(hour, min))
  # end for min
# end for hour



layout = html.Div([
    
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ## Select Plots:
    html.Div([
        html.Div(
                html.Label(
                "Select Plots:", style = {"paddingTop": "20px", "color": "black"}
            ), style = {"display": "inline-block", "width": "10%"}
        ),
        html.Div(
                dcc.Dropdown(
                id="dropdown-strain-time",
                options=DF_STRAINS.columns,
                value=[DF_STRAINS.columns[0], DF_STRAINS.columns[1]],
                multi=True
            ), style = {"display": "inline-block", "width": "50%"}
        ),
    ], style = {"marginTop": "35px"}),
    
    ## Graph:
    html.Div(
        dcc.Graph(id="strain-time-graph"),
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
                    id = "DatePickerSingle-strain-gradient-date",
                    min_date_allowed = DF_STRAINS.index[0],
                    max_date_allowed = DF_STRAINS.index[-1],
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
                    id="dropdown-strain-gradient-time",
                    options=times,
                    value=datetime.time(5, 0, 0),
                    multi=False,
                ), style = {"display": "inline-block", "width": "20%"}
            ),
            html.Div(style = {"display": "inline-block", "width": "10%"}),
        ]),
        
        ## Graph:
        html.Div(
            dcc.Graph(id="strain-gradient-graph"),
            style = {"position": "absolute", "alignment": "center"}
        ),
    ], style = {"display": "inline-block", "width": "40%"}
    ),
    html.Div(style = {"display": "inline-block", "width": "30%"}),
    
    
])




##################################################################################################################
# UPDATE STRAIN-TIME GRAPH:

@callback(
    Output("strain-time-graph", "figure"),
    Input("dropdown-strain-time", "value"),
)
def update_temp_time_graph(cols):
    
    df1 = DF_STRAINS[cols]
    
    fig1 = px.line(df1, template = "simple_white")
    
    fig1.update_layout(
        title_x = 0.5,
        xaxis_title = "Date",
        yaxis_title = "Strain [με]",
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
    Output("strain-gradient-graph", "figure"),
    Input("DatePickerSingle-strain-gradient-date", "date"),
    Input("dropdown-strain-gradient-time", "value"),
)
def update_temp_gradient_graph(date, time):
    
    datum = datetime.datetime(int(date.split("-")[0]), int(date.split("-")[1]), int(date.split("-")[2]),
                              int(time.split(":")[0]), int(time.split(":")[1]))
    
    
    y  = [75, 25]
    
    fig2 = go.Figure()
    
    
    if datum not in DF_STRAINS.index:
        plot_title = "Data not Available"
        fig2.add_trace(go.Scatter(x = [0],   y = [0], mode = "markers", name = "No Data"))
    else:
        df2 = DF_STRAINS.loc[datum].to_numpy()
        plot_title = str(datum)
        
        ## Reinforcement Location:
        fig2.add_hline(y = 50, line_width = 5, showlegend = True, line_color = "black",
                       name = "Reinfocement Location")
        
        ## Zero Strain:
        fig2.add_vline(x = 0, line_width = 5, showlegend = False, line_color = "black",
                       name = " ", line_dash = "dash")
        
        ## 0.5 %:
        fig2.add_trace(go.Scatter(x = df2[0:2],   y = y, mode = "markers", showlegend = False,
                                  name = "", marker_color = "blue", marker_size = 12))
        m = 50/(df2[0] - df2[1])
        c = 75 - (m*df2[0])
        x1 = (0 - c)/m
        x2 = (100 - c)/m
        fig2.add_trace(go.Scatter(x = [x1, x2],   y = [0, 100], mode = "lines", name = "0.5 %", 
                                  line_color = "blue"))
        
        ## 1.0 %:
        fig2.add_trace(go.Scatter(x = df2[2:4],   y = y, mode = "markers", showlegend = False,
                                  name = "", marker_color = "darkorange", marker_size = 12))
        m = 50/(df2[2] - df2[3])
        c = 75 - (m*df2[2])
        x1 = (0 - c)/m
        x2 = (100 - c)/m
        fig2.add_trace(go.Scatter(x = [x1, x2],   y = [0, 100], mode = "lines", name = "1.0 %", 
                                  line_color = "darkorange"))
        
        ## 2.0 %:
        fig2.add_trace(go.Scatter(x = df2[4:6],   y = y, mode = "markers", showlegend = False,
                                  name = "", marker_color = "green", marker_size = 12))
        m = 50/(df2[4] - df2[5])
        c = 75 - (m*df2[4])
        x1 = (0 - c)/m
        x2 = (100 - c)/m
        fig2.add_trace(go.Scatter(x = [x1, x2],   y = [0, 100], mode = "lines", name = "2.0 %", 
                                  line_color = "green"))
        
        ## 4.0 %:
        fig2.add_trace(go.Scatter(x = df2[6:8],   y = y, mode = "markers", showlegend = False,
                                  name = "", marker_color = "red", marker_size = 12))
        m = 50/(df2[6] - df2[7])
        c = 75 - (m*df2[6])
        x1 = (0 - c)/m
        x2 = (100 - c)/m
        fig2.add_trace(go.Scatter(x = [x1, x2],   y = [0, 100], mode = "lines", name = "4.0 %", 
                                  line_color = "red"))
    
    
    fig2.update_layout(
        title = plot_title,
        title_x = 0.5,
        xaxis_title = "Strain [με]",
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
