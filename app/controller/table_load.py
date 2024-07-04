from dash import callback, Output, Input, no_update, State, html, dcc, dash_table
import pandas as pd
from .azure import AzureWorkitems
from datetime import datetime


TABLE = None


@callback(
    Output("loading-table", "style"),
    Input("ok-pat", "n_clicks"),
    prevent_initial_call=True
)
def show_loading(_):
    return {'visibility': 'visible'}

def configDate(df):
    def try_parsing_date(text):
        formats = ['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ']
        for fmt in formats:
            try:
                return pd.to_datetime(text, format=fmt)
            except ValueError:
                pass
        raise ValueError('Nenhum formato de data correspondeu: ' + text)

    # Verificar se a coluna 'Data' está presente no DataFrame
    if 'Data' in df.columns:
        df['Data'] = df['Data'].apply(try_parsing_date)
        df['Data'] = df['Data'] - pd.Timedelta(hours=3) # corrigir fuso horario
        df['Data'] = df['Data'].dt.strftime('%d/%m/%Y %H:%M')
        df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y %H:%M')
    else:
        raise ValueError("Coluna 'Data' não encontrada no DataFrame")
    
    return df

@callback(
    Output("pat-configuration-div", "style"),
    Output("tablePlaceholder", "style"),
    Output("table-content", "data"),
    Output("loading-table", "style", allow_duplicate=True),
    Input("ok-pat", "n_clicks"),
    State("pat", "value"),
    prevent_initial_call=True,
)
def get_table(_, pat):
    global TABLE

    try:
        TABLE = AzureWorkitems(pat, 'DrogariaAraujo').get_all()
        df = pd.DataFrame(TABLE)
        df = configDate(df)
        return {'display': 'none'}, {'display': 'flex'}, df.to_dict('records'), {'visibility': 'hidden'}
    except Exception as e:
        print(f"Erro ao obter ou processar a tabela: {e}")
        return no_update, no_update, no_update, {'visibility': 'hidden'}

@callback(
    Output("tipo", "options"),
    Output("board", "options"),
    Output("state", "options"),
    Input("table-content", "data"),
    prevent_initial_call=True
)
def update_filters(table_data):
    if table_data:
        tipos = [{'label': tipo, 'value': tipo} for tipo in pd.DataFrame(TABLE)['Tipo'].unique()]
        boards = [{'label': board, 'value': board} for board in pd.DataFrame(TABLE)['Board'].unique()]
        states = [{'label': state, 'value': state} for state in pd.DataFrame(TABLE)['State'].unique()]
        return tipos, boards, states
    
    return [], [], []

@callback(
    Output("table-content", "data", allow_duplicate=True),
    Input("tipo", "value"),
    Input("board", "value"),
    Input("state", "value"),
    Input("date", "start_date"),
    Input("date", "end_date"),
    prevent_initial_call=True
)
def filter_table(selected_tipos, selected_boards, selected_states, start_date, end_date):
    df = pd.DataFrame(TABLE)
    df = configDate(df)

    if selected_tipos:
        df = df[df['Tipo'].isin(selected_tipos)]
    if selected_boards:
        df = df[df['Board'].isin(selected_boards)]
    if selected_states:
        df = df[df['State'].isin(selected_states)]

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        df = df[(df['Data'] >= start_date) & (df['Data'] <= end_date)]

    return df.to_dict('records')

@callback(
    Output("download-table", "data"),
    Input("btn-download-table", "n_clicks"),
    State("table-content", "data"),
    prevent_initial_call=True
)
def download_table(n_clicks, table_data):
    df = pd.DataFrame(table_data)
    return dcc.send_data_frame(df.to_csv, filename='table_data.csv', index=False)