import pandas as pd
import numpy as np
import pymysql

####################################### Acquire World Bank Data ################################

def get_contract_data():
    '''
    Returns a dataframe of World Bank project contracts.
    '''
    data = pd.read_csv('.\data\wb_contracts.csv')
    return data

####################################### MySQL Database #########################################
def get_connection(user='', password='', host='localhost', port='3306', database='worldbank'):
    '''
    Returns a formatted url to access a local SQL Database.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'