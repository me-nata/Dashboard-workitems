from dash import Dash, html, dcc, dash_table


TABLE_COMPONENT = dash_table.DataTable(
    data=None,
    id='table-content',
    sort_action="native",
    fixed_rows={'headers': True},
    style_table={'width': '100%', 'height': '400px', 'overflowY': 'auto', 'margin':'auto', 'overflowX': 'auto'},
    style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
    },
    style_cell={
        'textAlign': 'center',
        'padding': '10px',
        'maxWidth': '150px',
        'whiteSpace': 'normal',
    },
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ],
)