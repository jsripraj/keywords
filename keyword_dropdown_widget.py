from dash import Dash, html, dcc, Input, Output, State, callback
import neo4j_utils
import mysql_utils
import mongodb_utils
import closeness_widget

@callback(
    Output(component_id='kw_checklist', component_property='options'),
    Output(component_id='kw_hide', component_property='disabled'),
    Output(component_id='kw_reset', component_property='disabled'),
    Output(component_id='ins_checklist', component_property='options'),
    Output(component_id='ins_hide', component_property='disabled'),
    Output(component_id='ins_reset', component_property='disabled'),
    Output(component_id='faculty_dropdown', component_property='disabled'),
    Output(component_id='cytoscape', component_property='style'),
    Output(component_id='popularity_graph', component_property='figure'),
    Output(component_id='focus_graph', component_property='figure'),
    Input(component_id='keyword_dropdown', component_property='value'),
    State(component_id='faculty_dropdown', component_property='value'),
    prevent_initial_call=True
)
def keyword_selected(selected_keyword, faculty_id):
    kw_selected = selected_keyword is not None
    cyto_style = closeness_widget.shown_style if (kw_selected and faculty_id) else closeness_widget.hidden_style
    return (
        neo4j_utils.get_suggested_keywords(selected_keyword), # keyword checklist options
        not kw_selected, # keyword hide button
        not kw_selected, # keyword reset button
        neo4j_utils.get_suggested_institutes(selected_keyword), # institute checklist options
        not kw_selected, # institute hide button
        not kw_selected, # institute reset button
        not kw_selected, # faculty_dropdown
        cyto_style, # hide/show cytoscape
        mysql_utils.get_popularity_figure(selected_keyword) if kw_selected else {}, # popularity graph figure
        mongodb_utils.get_focus_figure(selected_keyword) if kw_selected else {}, # focus graph figure
    )
