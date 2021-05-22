import numpy as np
import pandas as pd


def prep_financial_report(df):
    '''
    
    '''
    date_col = df.columns[1]
    numeric_cols = df.columns[2:]

    df[date_col] = pd.to_datetime(df.loc[:,date_col])
    df[numeric_cols] = df.loc[:, numeric_cols].apply(pd.to_numeric,
                                                     downcast='float',
                                                     errors='coerce')
    df.fillna(0, inplace=True)
    
    return df