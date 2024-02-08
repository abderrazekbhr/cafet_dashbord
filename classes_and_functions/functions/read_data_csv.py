import pandas as pd
_DATA="static/data_base/Final_Dataset.csv"

def read_data_csv():
    data = pd.read_csv(_DATA)
    return data

def get_data_by_column(column_name):
    data=read_data_csv()
    return data[column_name]