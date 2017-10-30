
'''Script to grab parcel lat/longs from specified model and store all model lat/longs in Maps folder'''

import csv
import itertools
import pandas as pd
import numpy as np
from config import load
from aggregate import get_model_predictions
from access_postgres import get_mapping_data, concat_dataframe, insert_db

def create_violation_data(filename, csv_name):
    '''Input: Takes a file with all validation dates
       Output: Compiled csv of all parcel ids across on feature schema with violations, 
       inspections, unique violations, unique inspections, houses '''
       
    geo = get_coordinates()
    dates = pd.read_csv(filename)
    df = concat_dataframe(dates.validation_date.unique(), None, None, False)
    df['unique'] = df['parcel_id'] + '_' + df['date']
    merged = pd.merge(geo, df, on='parcel_id')  
    merged.to_csv(csv_name)

def get_coordinates():

    df = get_mapping_data()
    df = df.rename(index=str, columns= {'parcelid': 'parcel_id'})
    df.to_csv(PATH_TO_PARCEL_GEO)
    return df
    
def create_dummy_variables(old_file, new_file): 
    geo = pd.read_csv(old_file)
    geo['violation_dummy'] = np.where(geo['violations']> 0, 1, 0)
    geo['inspection_dummy'] = np.where(geo['inspections']> 0, 1, 0)
    df = geo[['parcel_id', 'unique', 'date', 'latitude', 'longitude', 'violation_dummy', 'inspection_dummy', 'violation_density', 'inspection_density']]
    df.to_csv(new_file)

    
def main(models_filename, violation_geo_file, dummy_file, models_of_interest, density_file, first_run=True):
    '''Input: file path of models
       Function reads in model filename and merges on uniqueParcel id with PATH_TO_DUMMY file 
       Output: Csv for individual models of interest with lat/long, violation dummy, inspection dummy, dummy variables for TP/TN'''
       
    if first_run:
        create_violation_data(models_filename, violation_geo_file)
        create_dummy_variables(violation_geo_file, dummy_file)

    validation_windows = {'31dec2014': 2, '31dec2015': 4}
    dummy = pd.read_csv(dummy_file)
    f = csv.reader(open(models_of_interest))
    for row in itertools.islice(f, 1, None):
        for date in validation_windows: 
            parcel_predict = get_model_predictions(row[validation_windows[date]], TOP_15PERCENT)
            parcel_predict['date'] = date
            parcel_predict['unique'] = parcel_predict['parcel_id'] + '_' + parcel_predict['date']   
            merged_df = pd.merge(parcel_predict, dummy, on='unique')  
            merged_df = merged_df.rename(index=str, columns={'parcel_id_x': 'parcel_id'})
            final = merged_df[['parcel_id', 'unique', 'latitude', 'longitude', 'violation_dummy', 'inspection_dummy', 'violation_density', 'inspection_density']] 
            name = str(row[1]) + '_' + date
            csv_name = ("Maps/{}.csv".format(name))
            final.to_csv(csv_name)
        
if __name__ == '__main__':
    
    params = load('models.yaml')['PARAMS']
    paths = load('models.yaml')['PATHS']
    
    WEIGHTS = params['WEIGHTS']
    TOP_15PERCENT = int(params['TOP_15PER']/2)
    MODEL_ID = params['MODEL_ID']
    DATE = params['DATE']
    
    PATH_TO_PARCEL_GEO = paths['PATH_TO_PARCEL_GEO']
    PATH_TO_DUMMY = paths['PATH_TO_DUMMY']
    PATH_TO_GEO_VIOLATIONS = paths['PATH_TO_GEO_VIOLATIONS']
    PATH_TO_MOI2 = paths['PATH_TO_MOI2']
    PATH_TO_MODELS = paths['PATH_TO_MODELS']
    PATH_TO_DENSITY = paths['PATH_TO_DENSITY']

    
    main(PATH_TO_MODELS, PATH_TO_GEO_VIOLATIONS, PATH_TO_DUMMY, PATH_TO_MOI2, PATH_TO_DENSITY, False)



