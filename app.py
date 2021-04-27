import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np
from scipy.stats import norm

app = dash.Dash(__name__)
server = app.server

colors= {
    "background": "White",
    "text": "#7FDBFF"
}

app.layout = html.Div(style={'backgroundColor': colors['background'], 'width': "100%", "display": "inline-block"}, children=[
    
    html.Div(style={'display': 'inline-block', 'width':'50%', 'float':'left'}, children=[
        dcc.Markdown('''
        # Sample Size Calculator
        
        Calculate required sample size and expected errors for a 2 response question given a simple random sampling method.

        The true value is the actual unknown value that the study is attempting to estimate. If there is no expectation as to what this might be prior to sampling, error is maximised at 50% so this is used as the default value.
        
        '''),
        
        html.Div(id='div2', children="Population Size"),
   
        dcc.Input(id='populationinput', value=1000, type='text'),
    
        html.Div(id='div1', children="Percentage in Population (True Value)"),

        dcc.Slider(id='propinput', min=0, max=100, step=1, value=50, marks={i: '{}%'.format(i) for i in range(0,105,5)}),

        html.Div(id='div3', children="Confidence"),
        dcc.Slider(id='confidenceinput', min=0, max=100, step=1, value=95, marks={i: '{}%'.format(i) for i in range(0,105,5)}),

        html.Div(id='div4', children="Target Error (Percentage Points)"),
        dcc.Slider(id='errorinput', min=0, max=100, step=1, value=5, marks={i: '{}%'.format(i) for i in range(0,105,5)})]),

    html.Div(
        dcc.Graph(
            id='EstimateGraph',
            style={'width': '100%'}
        ), style={'display': 'inline-block', 'width':'50%', 'float':'left'}),

    html.Div(
        dcc.Graph(
            id='ConfGraph',
            style={'width': '100%'}
        ), style={'display': 'inline-block', 'width':'50%', 'float':'left'}),

    html.Div(
        dcc.Graph(
            id='ErrorGraph',
            style={'width': '100%'}
        ), style={'display': 'inline-block', 'width': '50%', 'float':'left'})
    
])

@app.callback(
    Output(component_id='EstimateGraph', component_property='figure'),
    [Input(component_id='propinput', component_property='value'),
    Input(component_id='populationinput', component_property='value'),
    Input(component_id='confidenceinput', component_property='value'),
    Input(component_id='errorinput', component_property='value')
    ]
)
def update_output_div(percentage, population, confidence, errortarget):
    
    p = int(percentage)/100
    pop = int(population)
    c = int(confidence)/100
    et = int(errortarget)
    conf = 1-((1 - c)/2)

    x = np.array(range(10,pop+1))
    s = (p * (1-p)) / (x-1)
    f = 1 - (x/pop)
    se = (s*f)**(1/2)
    ci = se * norm.ppf(conf)
    ci_upper = (p+ ci)*100
    ci_lower = (p - ci)*100

    r = {
        'data': [
        {'x': x,
        'y': ci_upper,
        'name': 'Upper'},
        
        {'x': x,
        'y': ci_lower,
        'name': 'Lower'},

        ## Percentage Line
        {'x': [0,pop],
        'y': [p*100]*2,
        'name': 'Actual'}
    ],
    'layout': {
        'title': 'Estimate of Means',
        'xaxis': {
            'title': "Sample Size",
            'range': [0,pop]
        },
        'yaxis': {
            'title': 'Estimate (%)',
            'range': [0,100]
        }
    }
    }

    return r

@app.callback(
    Output(component_id='ConfGraph', component_property='figure'),
    [Input(component_id='propinput', component_property='value'),
    Input(component_id='populationinput', component_property='value'),
    Input(component_id='confidenceinput', component_property='value'),
    Input(component_id='errorinput', component_property='value')
    ]
)
def update_ConfGraph(percentage, population, confidence, errortarget):
    
    p = int(percentage)/100
    pop = int(population)
    c = int(confidence)/100
    et = int(errortarget)/100
    conf = norm.ppf(1-((1 - c)/2))

    x = np.array(range(10,pop+1))
    s = (p * (1-p)) / (x-1)
    f = 1 - (x/pop)
    se = (s*f)**(1/2)
    ci = (se * conf)*100

    pp = p*(1-p)
    sample_size = (conf**2 * pop * pp) / ((conf**2 * pp) + (pop * et**2))

    r = {
        'data': [
        {'x': x,
        'y': ci,
        'name': 'Confidence'},
        {'x': [sample_size]*2,
        'y': [0,20],
        'name': 'Required Sample Size'}
    ],
    'layout': {
        'title': 'Confidence Interval | Percentage',
        'xaxis': {
            'title': "Sample Size",
            'range': [0,pop]
        },
        'yaxis': {
            'title': 'Estimate (+-%)',
            'range': [0,20]
        }
    },

    }

    return r


@app.callback(
    Output(component_id='ErrorGraph', component_property='figure'),
    [Input(component_id='propinput', component_property='value'),
    Input(component_id='populationinput', component_property='value'),
    Input(component_id='confidenceinput', component_property='value'),
    Input(component_id='errorinput', component_property='value')
    ]
)
def update_ConfGraph(percentage, population, confidence, errortarget):
    
    p = int(percentage)/100
    pop = int(population)
    c = int(confidence)/100
    et = int(errortarget)/100
    conf = norm.ppf(1-((1 - c)/2))

    pp = p*(1-p)
    sample_size = (conf**2 * pop * pp) / ((conf**2 * pp) + (pop * et**2))

    x = np.linspace(0,1,101)
    s = (x * (1-x))/(sample_size-1)
    f = 1 - (sample_size/pop)
    se = (s*f)**(1/2)
    ci = (se * conf)*100
 
    r = {
        'data': [
        {'x': x*100,
        'y': ci,
        'name': 'Confidence'}

    ],
    'layout': {
        'title': 'Confidence Interval | Calculated Sample Size',
        'xaxis': {
            'title': "Occurance in Population (%)",
            'range': [0,100]
        },
        'yaxis': {
            'title': 'Estimate (+-%)',
            'range': [0,15]
        }
    },

    }

    return r

if __name__ == '__main__':
    app.run_server(debug=True)
