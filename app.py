# Run this app with `python3 app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output, State, callback
import dash_cytoscape as cyto
import plotly.graph_objs as go
import neo4j_utils
import mysql_utils
import keyword_dropdown_widget
import closeness_widget
import suggested_keywords_widget
import suggested_institutes_widget

app = Dash()

app.layout = html.Div([
    html.H1("Keyword Analyzer", style={'text-align': 'center'}),

    # Main keyword dropdown
    html.Div([
        html.Div(dcc.Dropdown(options=neo4j_utils.get_suggestable_keywords(), 
                              placeholder="Search for a keyword...", 
                              id='keyword_dropdown'),
                 style={'width': '30%'}), 
    ], style={'display': 'flex', 'justify-content': 'center'}),

    # First row
    html.Div(style={'display': 'flex'}, children=[
        # Focus widget
        html.Div(style={'width': '50%'}, children=[
            html.H2("Focus on Keyword"),
            html.Div(dcc.Graph(
                figure={},
                id='focus_graph',
            )),
            html.P("For selected keyword k, Focus attempts to measure how much k consumes the publications of interested faculty. "
                   "Each publication has a keyword score representing its association with that keyword. "
                   "Focus is calculated as the ratio of the cumulative score for k to the cumulative score for all keywords, "
                   "for all publications of the faculty who are interested in k.")
        ]),

        # Popularity widget
        html.Div(style={'width': '50%'}, children=[
            html.H2("Keyword Popularity Over Time"),
            html.Div(dcc.Graph(
                figure={},
                id='popularity_graph',
            )),
            html.P("hellow orld")
        ]),
    ]),

    # Second row
    # Closeness widget
    html.Div([
        html.H2("Faculty Closeness to Keyword"),
        html.Div(dcc.Dropdown(
            options=neo4j_utils.get_faculty(), 
            placeholder="Search for faculty...", 
            id='faculty_dropdown', 
            disabled=True
        )),
        html.Div([
            cyto.Cytoscape(
                id='cytoscape',
                layout={'name': 'cose'},
                style=closeness_widget.hidden_style,
                elements=[],
                stylesheet=[
                    # Group selectors
                    {
                        'selector': 'node',
                        'style': {
                            'content': 'data(label)'
                        }
                    },

                    # Class selectors
                    {
                        'selector': '.faculty',
                        'style': {
                            'background-color': 'lightgreen',
                            'line-color': 'green'
                        }
                    },
                    {
                        'selector': '.keyword',
                        'style': {
                            'background-color': 'skyblue',
                            'line-color': 'blue'
                        }
                    },
                    {
                        'selector': '.edge',
                        'style': {
                            'background-color': 'gold',
                            'line-color': 'red'
                        }
                    }
                ]
            )
        ])
    ]),

    # Third row
    html.Div(style={'display': 'flex'}, children=[
        # Trending widget
        html.Div(style={'width': '50%'}, children=[
            html.H2("Top Trending Keywords"),
            html.Div(dcc.Graph(
                figure=mysql_utils.get_trending_figure(),
                id='trending_graph',
            ))
        ]),

        # Suggested keywords widget
        html.Div(style={'width': '25%', 'display': 'flex', 'justify-content': 'center'}, children=[
            html.Div(children=[
                html.H2("Suggested Keywords"),
                html.Div(dcc.Checklist([], id='kw_checklist')),
                html.Button('Hide Selected', id='kw_hide', disabled=True),
                html.Button('Reset Hidden', id='kw_reset', disabled=True)
            ])
        ]),

        # Suggested institutes widget
        html.Div(style={'width': '25%', 'display': 'flex', 'justify-content': 'center'}, children=[
            html.Div(children=[
                html.H2("Suggested Institutes"),
                html.Div(dcc.Checklist([], id='ins_checklist')),
                html.Button('Hide Selected', id='ins_hide', disabled=True),
                html.Button('Reset Hidden', id='ins_reset', disabled=True)
            ])
        ]),
    ])
])

if __name__ == '__main__':
    app.run(debug=True)
