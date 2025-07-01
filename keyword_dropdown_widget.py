from dash import Dash, html, dcc, Input, Output, State, callback
import neo4j_utils
import mysql_utils
import mongodb_utils
import closeness_widget

@callback(
    Output(component_id='kw_table', component_property='data'),
    Output(component_id='kw_hide', component_property='disabled'),
    Output(component_id='kw_reset', component_property='disabled'),
    Output(component_id='ins_table', component_property='data'),
    Output(component_id='ins_hide', component_property='disabled'),
    Output(component_id='ins_reset', component_property='disabled'),
    Output(component_id='faculty_dropdown', component_property='disabled'),
    Output(component_id='cytoscape', component_property='style'),
    Output(component_id='cytoscape', component_property='elements'),
    Output(component_id='popularity_graph', component_property='figure'),
    Output(component_id='focus_graph', component_property='figure'),
    Output(component_id='focus_keyword_span', component_property='children'),
    Output(component_id='popularity_keyword_span', component_property='children'),
    Output(component_id='closeness_keyword_span', component_property='children'),
    Input(component_id='keyword_dropdown', component_property='value'),
    State(component_id='faculty_dropdown', component_property='value'),
    State(component_id='faculty_dropdown', component_property='options'),
    prevent_initial_call=True
)
def keyword_selected(selected_keyword, faculty_id, faculty_options):
    kw_selected = selected_keyword is not None
    cyto_style = closeness_widget.shown_style if (kw_selected and faculty_id) else closeness_widget.hidden_style
    header_word = selected_keyword if kw_selected else 'Keyword'
    faculty_label = closeness_widget.get_faculty_label(faculty_id, faculty_options)
    return (
        neo4j_utils.get_suggested_keywords(selected_keyword), # keyword table data
        not kw_selected, # keyword hide button
        not kw_selected, # keyword reset button
        neo4j_utils.get_suggested_institutes(selected_keyword), # institute table data
        not kw_selected, # institute hide button
        not kw_selected, # institute reset button
        not kw_selected, # faculty_dropdown
        cyto_style, # hide/show cytoscape
        neo4j_utils.get_shortest_path(faculty_id, selected_keyword), # cytoscape
        mysql_utils.get_popularity_figure(selected_keyword) if kw_selected else {}, # popularity graph figure
        mongodb_utils.get_focus_figure(selected_keyword) if kw_selected else {}, # focus graph figure
        header_word, # focus keyword span
        header_word, # popularity keyword span
        header_word, # closeness keyword span
    )
