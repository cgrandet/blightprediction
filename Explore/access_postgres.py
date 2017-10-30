
import os
import pandas as pd
from config import main, load
from psycopg2 import connect
from sqlalchemy import create_engine


def make_connection():
    conn = connect(host=main['db']['host'], user=main['db']['user'], password=main['db']['password'], 
               database=main['db']['database'], port=main['db']['port'])
    return conn
    
def access_features(query, params=None):
    conn = make_connection()
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df
    
def concat_dataframe(schema_list, space_delta, time_delta, params =False):
    ##if params = False, function simply uses default of 400 m, 12 months as default feature windows
    all_data = []

    for date in schema_list:
        if not params: 
            table_schema = 'features' + '_' + (str(date)).lower() 
            table = 'neighborhood_score' + '_' + '400m' + '_' + '12months'
            schematable = table_schema + '.' + table
            query = '''SELECT parcel_id, violations, inspections, unique_violations, unique_inspections, houses FROM {} '''.format(schematable)
            try:    
                df = access_features(query, None)
                df['date'] =  (str(date)).lower() 
                all_data.append(df)
        
            except:
                pass
    df = pd.concat(all_data, axis=0, ignore_index=True)
    df['inspection_density'] = df['unique_inspections']/df['houses']
    df['violation_density'] = df['unique_violations']/df['houses']
    
    return df
  
     
def get_mapping_data():
    '''Grabs all parcel ids with latitude/longitude from Postgres'''
 
    query = '''SELECT parcelid, latitude, longitude FROM shape_files.parcels_cincy '''
    return access_features(query, None)
    
    
def insert_db():
    connparams = load('config.yaml')['db']
    uri = '{dialect}://{user}:{password}@{host}:{port}/{database}'.format(**connparams)
    engine = create_engine(uri)
    return engine
    
    