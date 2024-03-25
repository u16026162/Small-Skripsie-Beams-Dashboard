import dash
from dash import html, dcc
import dash_bootstrap_components as dbc







app = dash.Dash(
    
    __name__,
    
    external_stylesheets = [
        dbc.themes.CERULEAN
    ],
    
    title = "Small Skripsie Beams",
    
    use_pages = True
    
)



Navbar = dbc.Nav([
    
    dbc.NavLink([
        
        html.Div(page["name"], className = "ms-2")
        
    ], href = page["path"], active = "exact",
    
    ) for page in dash.page_registry.values()
    
    
    ],
    
    vertical = False,
    pills = True,
    className = "nav-justified"
    
)













app.layout = html.Div(
    [
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Main Header:
        
        ## Heading:
        html.H1("Small Skripsie Beams", 
                style = {
                    "fontsize": 100, 
                    "textAlign":"center", 
                    "family": "Arial",
                    "color": "black"
                }
        ),
        
        
        ## Links:
        html.Div([
            
            html.Div(style = {"display": "inline-block", "width": "25%"}),
            html.Div(Navbar, style = {"display": "inline-block", "width": "50%", "location": "center"}),
            html.Div(style = {"display": "inline-block", "width": "25%"})
            
        ]),
        
        # Line
        html.Hr(
            style = {"height": "2px", "color": "black", "border": "none", "backgroundColor": "black"}
        ),
        
        
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Content of each page:
        
        dash.page_container
        
        
    ]
)












if __name__ == "__main__":
    app.run(debug = True)