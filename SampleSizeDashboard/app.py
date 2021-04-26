import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

app = dash.Dash()

colors= {
    "background": "White",
    "text": "#7FDBFF"
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.Div(id='divcont', children="Percentage in Population"),
    dcc.Slider(id='propinput', min=0, max=100, step=1, value=50, marks={i: '{}%'.format(i) for i in range(0,110,10)}),
    
    html.Div(id='divcont2', children="Population Size"),
    dcc.Input(id='populationinput', value=1000, type='text'),

    dcc.Graph(
        id='Graph1'
    ) 
])

@app.callback(
    Output(component_id='Graph1', component_property='figure'),
    [Input(component_id='propinput', component_property='value'),
    Input(component_id='populationinput', component_property='value')]
)
def update_output_div(input_prop, input_pop):
    
    x = int(input_prop)
    y = int(input_pop)

    r = {
        'data': [
        {'x': [x, x+2, x+3],
        'y': [x, x*1.2, x*1.1],
        'name': 'Confidence'},
        
        ## Percentage Line
        {'x': [0,y],
        'y': [input_prop]*2,
        'name': 'Actual'}
    ],
    'layout': {
        'title': 'Estimate of Means',
        'xaxis': {
            'title': "Sample Size",
            'range': [0,y]
        },
        'yaxis': {
            'title': 'Estimate (%)',
            'range': [0,100]
        }
    }
    }

    return r

if __name__ == '__main__':
    app.run_server(debug=True)