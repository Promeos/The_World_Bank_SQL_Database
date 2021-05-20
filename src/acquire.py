import pandas as pd
import requests
import os

###################### REST API Functions ######################
def base_url():
    '''
    Returns base url to acquire financial data.
    
    Parameters
    ----------
    None
    
    Returns
    -------
    string url to acquire data using alphavantage REST API.
    '''
    return 'https://www.alphavantage.co/query?'


def response_endpoint(endpoint):
    '''
    Accepts endpoint to a [placeholder].
    
    Returns 
    Parameters
    ----------
    endpoint : str
        
    Returns
    -------
    requests.models.Response object
    '''
    get_request = requests.get(base_url() + endpoint)
    return get_request


def check_local_cache(data):
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
    file_name = f'{data}.csv'
    
    if os.path.isfile(file_name):
        return pd.read_csv(file_name, index_col=False)
    else:
        return False



###################### Acquire Financial Reports ######################
def acquire_financials(report_name='INCOME_STATEMENT'):
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
    cache = check_local_cache(data=report_name)
    
    if cache is False:
        path = f'function={report_name}'
        endpoint = response_endpoint(path)
        
        # CREATE FUNCTION
        
        df.reset_index(drop=True, inplace=True)
        df.to_csv(f'{report_name}.csv', index=False)
        return df
    else:
        return cache