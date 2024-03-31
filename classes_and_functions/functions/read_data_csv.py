import pandas as pd
_DATA="static/data_base/Final_Dataset.csv"
_GRID="classes_and_functions/csv/grid.csv"
_PREDICT="classes_and_functions/csv/prediction.csv"

def read_data_csv():
    data = pd.read_csv(_DATA)
    return data

def get_data_by_column(column_name):
    data=read_data_csv()
    return data[column_name]

def get_data_by_column_grid(columns):
    data = pd.read_csv(_GRID)
    return data[columns]

def get_data_by_column_predict(columns):
    data = pd.read_csv(_PREDICT)
    return data[columns]