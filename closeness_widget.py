from dash import Dash, html, dcc, Input, Output, State, callback
import neo4j_utils

hidden_style = {'width': '100%', 'height': '0px'}
shown_style = {'width': '100%', 'height': '400px'}

@callback(
    Output(component_id='cytoscape', component_property='elements', allow_duplicate=True),
    Output(component_id='cytoscape', component_property='style', allow_duplicate=True),
    Output(component_id='closeness_header', component_property='children', allow_duplicate=True),
    Input(component_id='faculty_dropdown', component_property='value'),
    State(component_id='keyword_dropdown', component_property='value'),
    State(component_id='faculty_dropdown', component_property='options'),
    prevent_initial_call=True,
)
def faculty_selected(faculty_id, keyword, faculty_options):
    show_cyto = shown_style if (faculty_id and keyword) else hidden_style
    faculty_label = get_faculty_label(faculty_id, faculty_options)
    return (
        neo4j_utils.get_shortest_path(faculty_id, keyword), 
        show_cyto,
        'Distance from ' + (faculty_label if faculty_label else 'Faculty') + ' to ' + keyword
    )

def get_faculty_label(fac_id: str, fac_options: list) -> str:
    for option in fac_options:
        if option['value'] == fac_id:
            return option['label']
    return ''
