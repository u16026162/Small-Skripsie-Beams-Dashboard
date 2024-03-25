import dash
from dash import dcc, html, callback, Output, Input

import os, datetime

import pandas as pd, numpy as np
import plotly.express as px
import plotly.graph_objects as go

from PIL import Image

dash.register_page(__name__, name = "Home", path = "/")



image_list = [f for f in os.listdir(os.getcwd() + "/data/images")]



layout = html.Div([
    
    html.Div(html.Label("Last update: 2024-03-25", style = {"verticalAlign": "top"}),
             className = "align-top",
             style = {"display": "inline-block", "width": "30%", "color": "black"}),
    html.Div([
        html.Img(
            src = Image.open(os.getcwd()+"/data/images/"+img), 
            style = {"width": "100%", "paddingTop": "20px"}
        ) for img in image_list
        ], style = {"display": "inline-block", "width": "40%"}
    ),
    html.Div(style = {"display": "inline-block", "width": "30%"}),
    
])