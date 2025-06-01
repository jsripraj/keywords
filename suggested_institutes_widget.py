from dash import Dash, html, dcc, Input, Output, State, callback
import neo4j_utils

@callback(
    Output(component_id='ins_checklist', component_property='options', allow_duplicate=True),
    Input(component_id='ins_hide', component_property='n_clicks'),
    State(component_id='keyword_dropdown', component_property='value'),
    State(component_id='ins_checklist', component_property='value'),
    prevent_initial_call=True,
)
def institute_hide_selected_clicked(n_clicks, seed_keyword, to_hide):
    neo4j_utils.hide_institutes(to_hide)
    return neo4j_utils.get_suggested_institutes(seed_keyword)

@callback(
    Output(component_id='ins_checklist', component_property='options', allow_duplicate=True),
    Output(component_id='ins_checklist', component_property='value'),
    Input(component_id='ins_reset', component_property='n_clicks'),
    State(component_id='keyword_dropdown', component_property='value'),
    prevent_initial_call=True
)
def institute_reset_hidden_clicked(n_clicks, seed_keyword):
    neo4j_utils.unhide_all_institutes()
    return neo4j_utils.get_suggested_institutes(seed_keyword), []
