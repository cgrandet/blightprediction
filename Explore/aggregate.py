import os
import csv
import itertools
import pandas as pd
import time
from access_postgres import concat_dataframe

MODEL_ID = 1
DATE = 2
SPACE_DELTA = 3
TIME_DELTA = 4
TOP_15PER = 31588/2  
TEMP = 'Data/temp.csv'
FINAL = 'Data/final_output.csv'

path_to_predictions = "/mnt/data/economic_development/cincinnati_blight/output/output_nov_2016/top_predictions_on_all_parcels/"
file_path = "/mnt/data/economic_development/MLPPLab-Cincinnati/LAB/data_for_postgres.csv"

def get_model_predictions(model, k):
    ##Input: list of model ids, k-number of rows from model prediction table
    ## Params: If not F, function grabs all rows 
    ##Output: Model's inspection date, parcel_ids, prediction scores
    
    if k: 
        return pd.read_csv(os.path.join(path_to_predictions, model), nrows=k, usecols=['inspection_date', 'parcel_id', 'prediction'])
      
    else: 
        return pd.read_csv(os.path.join(path_to_predictions, model), usecols=['inspection_date', 'parcel_id', 'prediction'])

def write_out_results(result_list, temp_csv):
    with open(temp_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(result_list)
        
def merge_data(temp_csv, final_name, filename):
    original = pd.read_csv(filename)
    temp = pd.read_csv(temp_csv)
    merged = pd.merge(original, temp, on='model_id')
    merged.to_csv(final_name)
    
def grab_and_go(df, parcel_df):
    merged = pd.merge(df, parcel_df, on='unique')
    return merged['violations'].mean(), merged['inspections'].mean(), merged['houses'].mean(), merged['inspection_density'].mean(), merged['violation_density'].mean()
   
def aggregator(filename):
    start = time.time()
    dates = pd.read_csv(filename)
    df = concat_dataframe(dates.validation_date.unique(), None, None, False)
    df['unique'] = df['parcel_id'] + '_' + df['date']
    data = []
    f = csv.reader(open(filename))

    for row in itertools.islice(f, 1, None):
        try: 
            parcel_predict = get_model_predictions(row[MODEL_ID], TOP_15PER)
            prediction_mean = parcel_predict['prediction'].mean()
            parcel_predict['unique'] = parcel_predict['parcel_id'] + '_' + (str(row[DATE]).lower())    
            violations, inspections, houses, inspection_density, violation_density  = grab_and_go(df, parcel_predict)
            data.append([row[MODEL_ID], (str(row[DATE]).lower()), prediction_mean, violations, inspections, houses, inspection_density,   violation_density])
                
        except: 
            print("Serious issues")
      
    end = time.time()
    print ("Process took {} seconds".format(end-start))   
    header = [['model_id', 'date', 'prediction', 'violations', 'inspections', 'houses', 'inspection_density', 'violation_density']]
    merged = header + data 
    write_out_results(merged, TEMP)
    merge_data(TEMP, FINAL, file_path) 
    
if __name__ == '__main__':
       
## this function to create merged postgres data
##aggregator(file_path)
  merge_data(TEMP, FINAL, file_path)  
