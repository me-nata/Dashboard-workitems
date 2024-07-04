from dash import Dash, html, dcc
from .table import TABLE_COMPONENT


app = Dash()
app.layout = [
    html.Div([ 
        html.Div([
            html.Label('Personal Acess Token', key='pat'),
            dcc.Input(id='pat', placeholder='Digite...')
        ], className='tagInput'),
        html.Div([
            html.Div([
                html.Div([
                    html.Div(className='loader'),
                    html.P('Isso pode levar alguns minutos...')
                ], id='loading-table'),
            ]),
            html.Button('Ok', id='ok-pat'),
        ], id='div-button'),
    ], id='pat-configuration-div'),
    html.Div([
        html.Div([
            html.Div([
                html.Label('Tipo'),
                dcc.Dropdown(
                    multi=True,
                    id='tipo'
                )
            ], className='tagInput'),
            html.Div([
                html.Label('Board'),
                dcc.Dropdown(
                    multi=True,
                    id='board'
                )
            ], className='tagInput'),
            html.Div([
                html.Label('State'),
                dcc.Dropdown(
                    multi=True,
                    id='state'
                )
            ], className='tagInput'),
            html.Div([
                html.Label('Data'),
                dcc.DatePickerRange(
                    start_date_placeholder_text="De",
                    end_date_placeholder_text="Até",
                    calendar_orientation='vertical',
                    display_format='DD/MM/YYYY',
                    id='date',
                    style={'transform':'scale(0.7)'}
                )
            ], className='tagInput'),
        ], id='filters'),
        html.Button("Baixar Tabela", id="btn-download-table"),
        dcc.Download(id="download-table"),
        TABLE_COMPONENT
    ], id='tablePlaceholder'),

    dcc.Location(id='url', refresh=True)
]