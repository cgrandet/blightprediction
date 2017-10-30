# MLPPLab-Cincinnati
Carlos Grandet and Charity King

## A Post-Model Evaluation of the ongoing DSSG Cincinnati Blight Prediction Project:
First settled in 1788, Cincinnati is one of the oldest American cities west of the original colonies. Today, the city struggles with aging home stock, stifling economic redevelopment in some neighborhoods. DSSG is working with the City of Cincinnati to identify properties at risk of code violations or abandonment. 

This project's scope is to map out past blight prediction modeling based on the desired parameter:
  * Homes in low-violation density areas
  * Homes in low-inspection density areas
  * High Accuracy
  * Model Stability at different precision rates
  
## Clone Repo
Clone the repo in `$ROOT_FOLDER`

`git clone https://github.com/dssg/MLPPLab-Cincinnati.git`

## Installation

We're using Python 2.7X Download Anaconda
Download the environment_class.yml
Create an environment with:

`conda env create -f environment_class.yml`

Activate the collectionname of the environment

`source activate cincinnati_class`

## Database Credentials

We are using the `config.yaml` to hold the sensitive login information for the inspection/feature data in Postgres and the model results in MongoDB. 
```
:db:
  dialect: 'postgresql'
  host: 'postgres.dssg.io.'
  user: 'cincinnati_class'
  password: XXXXXXXXXXXXXXXXXX
  database: 'cincinnati_blight'
  port: 5432

logger:
  uri: XXXXXXXXXXXXXXXXXXXXX
  db: 'models'
  collection: 'cincinnati'
```

The `config.py` file is a method to extract the dictionary information out of `config.yaml`

## Other Configurations

We are using the file `models.yaml` to store code-specific parameters, such as file column names, file paths, weighting schemes, etc. Any global variables used should be stored in this file. 

```
PARAMS: 
  WEIGHTS: [[0.2, 0.2, 0.2, 0.2, 0.2], [1.0, 0, 0, 0, 0], [0.5, 0.5, 0, 0, 0], [0.5, 0.3, 0.2, 0, 0]] 
  LENGTH: 31588
  MODEL_ID: 1
  DATE: 2
  SPACE_DELTA: 3
  TIME_DELTA: 4

PATHS:
  PATH_TO_PARCEL_GEO:  "Data/all_parcels_geo.csv"
  PATH_TO_DUMMY: "Data/violation_dummy.csv"
  PATH_TO_GEO_VIOLATIONS:  "Data/violation_geo.csv"
  PATH_TO_MOI2:  "/mnt/data/economic_development/MLPPLab-Cincinnati/LAB/maps_validation_window.csv"
  PATH_TO_MOI:  "/mnt/data/economic_development/MLPPLab-Cincinnati/LAB/models_for_maps.csv"
  PATH_TO_MODELS: "/mnt/data/economic_development/MLPPLab-Cincinnati/LAB/data_for_postgres.csv"
  PATH_TO_DENSITY: "Data/final_output.csv" 
```

## Code

To aggregate all data used for model analysis, run `python eval.py`


`eval.py` : This is the main wrapper function to aggregate all data used for analysis. It calls the following component functions:

*  `get_csv.py` : Scrapes the Cincinnati MongoDB and dumps all evaluation data into a csv. 

*  `clean_data.py` : Processes nested `get_csv.py` output into a standard relational table.

*  ` aggregate.py` : Grabs all model data for `clean_data.py` output

  * `aggregator()` : Uses all validation windows in data passed to scrape all Postgres data, returns all parcel ids for all validations windows as on dataframe with : parcel_id, inspections, violations, inspection density, violation density --> creates mean values for each model, converts to a temporary csv.
  
  *  `merge_data()` : Merges new dataframe from aggregator with csv of all models for further model selection based on violation density, inspection density, etc. 

* `run.py` : Last function that receives a .csv of models of interest and creates a model-specific .csv with violation density, inspection density, lat/longs, True Positive status. 

  * aggregates data
     * creates a main inspection violation dataframe of all parcels, with a unique column concatenating a parcelid with validation date. 
     * grabs geocoordinates for all parcels in postgres and JOINS on parcel_id in violation df
     * creates inspection/violation dummy columns in violation df
     
  * Iterates through a csv of selected models and for each model:
     * Grabs the top K% of predicted parcels
     * Merges predicted parcel DF with violation dataframe on "unique" column (parcel_id || validation date)
     * Output is a list of model df's with parcel id, lat, long, TP dummy, Inspection Dummy. 
     * Each model is saved as a csv with the name of the weight parameter that a specific model is optimized for with the validation            window. 


