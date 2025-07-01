# Run this app with `python3 app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output, State, callback, dash_table
import dash_cytoscape as cyto
import plotly.graph_objs as go
import neo4j_utils
import mysql_utils
import keyword_dropdown_widget
import closeness_widget
import suggested_keywords_widget
import suggested_institutes_widget

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children=[html.Span('Keyword', className='keyword'), " Analyzer"]),

    # Main keyword dropdown
    html.Div(className="center-content", children=[
        html.Div(dcc.Dropdown(options=neo4j_utils.get_suggestable_keywords(), 
                              placeholder="Search for a keyword...", 
                              id='keyword_dropdown'),
                 style={'width': '30%'}), 
    ]),

    # First row
    html.Div(style={'display': 'flex'}, children=[
        # Focus widget
        html.Div(className="card", style={'width': '50%'}, children=[
            html.H2(["Focus on ", html.Span('Keyword', className='keyword', id='focus_keyword_span')]),
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
        html.Div(className="card", style={'width': '50%'}, children=[
            html.H2(["Popularity of ", html.Span('Keyword', className='keyword', id='popularity_keyword_span')]),
            html.Div(dcc.Graph(
                figure={},
                id='popularity_graph',
            )),
        ]),
    ]),

    # Second row
    # Closeness widget
    html.Div(className="card", children=[
        html.H2(["Distance from ", 
                 html.Span('Faculty', className='faculty', id='closeness_faculty_span'), 
                 " to ", 
                 html.Span('Keyword', className='keyword', id='closeness_keyword_span')]),
        html.Div(className="center-content", children=[
            html.Div(style={'width': '30%'}, children=[
                dcc.Dropdown(
                    options=neo4j_utils.get_faculty(), 
                    placeholder="Search for faculty...", 
                    id='faculty_dropdown', 
                    disabled=True,
                )
            ]),
        ]),
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
                            'background-color': 'DarkGreen',
                        }
                    },
                    {
                        'selector': '.keyword',
                        'style': {
                            'background-color': 'DarkRed',
                        }
                    },
                    {
                        'selector': '.edge',
                        'style': {
                            'line-color': 'LightBlue'
                        }
                    }
                ]
            )
        ])
    ]),

    # Third row
    html.Div(style={'display': 'flex'}, children=[
        # Trending widget
        html.Div(className="card", style={'width': '50%'}, children=[
            html.H2("Top Trending Keywords"),
            html.Div(dcc.Graph(
                figure=mysql_utils.get_trending_figure(),
                id='trending_graph',
            ))
        ]),

        # Suggested keywords widget
        html.Div(className="card", style={'width': '25%', 'display': 'flex', 'justify-content': 'center'}, children=[
            html.Div(children=[
                html.H2("Suggested Keywords"),
                html.Div(dash_table.DataTable(
                    columns=[{'name': 'Keyword', 'id': 'Keyword'}], 
                    style_as_list_view=True, 
                    style_cell={'textAlign': 'left'}, 
                    style_header={
                        'backgroundColor': 'lightgray',
                        'fontWeight': 'bold'
                    },
                    id='kw_table')
                ),
                html.Div(style={'display': 'flex', 'justify-content': 'center'}, children=[
                    html.Button('Hide Selected', className="button", id='kw_hide', disabled=True),
                    html.Button('Reset Hidden', className="button", id='kw_reset', disabled=True)
                ])
            ])
        ]),

        # Suggested institutes widget
        html.Div(className="card", style={'width': '25%', 'display': 'flex', 'justify-content': 'center'}, children=[
            html.Div(children=[
                html.H2("Suggested Institutes"),
                html.Div(dash_table.DataTable(
                    columns=[{'name': 'Institute', 'id': 'Institute'}], 
                    style_as_list_view=True, 
                    style_cell={'textAlign': 'left'}, 
                    style_header={
                        'backgroundColor': 'lightgray',
                        'fontWeight': 'bold'
                    },
                    id='ins_table')
                ),
                html.Div(style={'display': 'flex', 'justify-content': 'center'}, children=[
                    html.Button('Hide Selected', className="button", id='ins_hide', disabled=True),
                    html.Button('Reset Hidden', className="button", id='ins_reset', disabled=True)
                ])
            ])
        ]),
    ])
])

if __name__ == '__main__':
    app.run(debug=True)
