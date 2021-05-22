import numpy as np
import pandas as pd
import requests
import os
from env import key

# Create a global variable to hold the apikey path
API_KEY_PATH = '&apikey={key}'

###################### REST API Functions ######################
#### RUN LPRUN% to test processing speed of a accessing a global variable
# in a function vs. calling a function within a function to access a variable.
def base_url():
    '''
    Base url to acquire financial data from Alphavantage.
    
    Parameters
    ----------
    None
    
    Returns
    -------
    url : str
        URL to acquire data using Alphavantage REST API.
    '''
    url = 'https://www.alphavantage.co/query?'
    return url


def report_endpoint(report, ticker):
    '''
    Endpoint to a acquire data using Alphavantage REST API.
    
    Parameters
    ----------
    data : str, default 'INCOME_STATEMENT'

    ticker : str, default 'IBM'
        
    Returns
    -------
    response : requests.models.Response object
        Response object with data from a specified endpoint.
    '''
    global API_KEY_PATH

    function = f'function={report}'
    symbol = f'&symbol={ticker}'
    file_type = '&datatype=csv'

    endpoint = function + symbol + API_KEY_PATH + file_type

    response = requests.get(base_url() + endpoint)
    return response


def extract_json(response):
    '''
    Extract quarterly data from the Response object
    '''
    data = response.json()
    q_data = data.get('quarterlyReports')

    return q_data


def report_dataframe(data, ticker):
    '''
    Transform the dictionary into a Pandas DataFrame, sorted by `fiscalDateEnding`
    '''
    df = pd.DataFrame(data)
    df.insert(0, 'ticker', ticker)
    df.drop(columns='reportedCurrency', inplace=True)
    df = df.sort_values('fiscalDateEnding').reset_index(drop=True)
    return df


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


def check_local_cache(file_name):
    '''
    Accepts an endpoint from [link] and checks to see if a local
    cached version of the data exists
    
    Returns endpoint data as a pandas DataFrame if a local cache exists
    Returns False if a local cache does not exist.
    
    Parameters
    ----------
    data : str
        
    Returns
    -------
    Return cached file as a pandas DataFrame if : os.path.isfile(file_name) == True
    Return False otherwise
    '''    
    if os.path.isfile(file_name):
        data = pd.read_csv(file_name, infer_datetime_format=True)
        data = data.convert_dtypes()
        return data
    else:
        return False


###################### Acquire Financial Reports ######################
def get_financial_data(ticker='IBM', report_name='INCOME_STATEMENT'):
    '''
    Acquires financial reports from 'https://www.alphavantage.co/' using REST API
    
    Return a financial report as a pandas Dataframe.
    
    Datasets
    --------
    'income_statement'
    'balance_sheet'
    'cashflow'

    Parameters
    ----------
    report_name : str, default 'INCOME_STATEMENT'
    
        Financial Reports
        -----------------
        'INCOME_STATEMENT': acquires incomes statement data
        'BALANCE_SHEET' : acquires balance sheet data
        'CASH_FLOW' : acquires cash flow data
    
    Returns
    -------
    pandas DataFrame
    '''
    file_name = f'./data/{ticker.lower()}_{report_name.lower()}.csv'

    cache = check_local_cache(file_name)
    
    if cache is False:
        response = report_endpoint(report=report_name, ticker=ticker)
        report = extract_json(response)
        df = report_dataframe(report, ticker=ticker)
        df = prep_financial_report(df)
        df.to_csv(file_name, index=False)
        return df
    else:
        return cache