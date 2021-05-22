import mysql.connector
import env


def get_connection(db, user=env.user, host=env.host, password=env.password):
    '''
    Returns a formatted url to access a SQL database.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'