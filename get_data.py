import json
import pandas as pd
from time import sleep
from utils import get_file

def get_sheet_data(path):
    if path.endswith(".xlsx") or path.endswith(".xls"):
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path)
    return [dict(row) for index, row in df.iterrows()]