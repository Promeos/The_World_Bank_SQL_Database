import pandas as pd
import pymysql


####################################### Acquire World Bank Data ################################
def get_contract_data():
    '''
    Returns a dataframe of World Bank contracts.
    '''
    data = pd.read_csv('./data/raw/wb_contracts.csv')
    return data


def get_project_data():
    '''
    Returns a dataframe of World Bank project.
    '''
    data = pd.read_excel('./data/raw/wb_projects.xlsx', engine='openpyxl', skiprows=[0, 2])
    return data


####################################### MySQL Database #########################################
def get_connection(user='', password='', host='localhost', port='3306', database='worldbank'):
    '''
    Returns a formatted url to access a local SQL Database compatible with Pandas `to_sql()` function.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'


def get_cursor(user='', password=''):
    '''
    Creates a connection to a MySQL database and returns the connection and a Cursor Object to interact with the database.
    '''
    cnx = pymysql.connect(user=user, password=password, host='localhost', port=3306)
    cursor = cnx.cursor()

    return cnx, cursor