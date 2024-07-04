from dash import Input, Output, State, callback, no_update


# Callback para redirecionar ao clicar duas vezes na linha
@callback(
    Output('url', 'href'),
    Input('table-content', 'active_cell'),
    State('table-content', 'data')
)
def update_url(active_cell, rows):
    if active_cell:
        row = active_cell['row']
        return rows[row]['Link']
    
    return no_update
