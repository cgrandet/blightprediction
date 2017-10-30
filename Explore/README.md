##Synopsis

This folder contains functions that:
* aggregate parcel ids on post-model predicted parcels for blight violations
* aggregate geocoordinate data for all parcel ids
* calculate inspection and violation density for each predicted parcel within the validation window of the experiment
* maps selected models color-coded for True Positive/False Positive violation predictions

##Code

The central file is `run.py` The `main()` in run.py:
* aggregates data
  * creates a main inspection violation dataframe of all parcels, with a unique column concatenating a parcelid with validation date. 
  * grabs geocoordinates for all parcels in postgres and JOINS on parcel_id in violation df
  * creates inspection/violation dummy columns in violation df
* Iterates through a csv of selected models and for each model:
  * Grabs the top K% of predicted parcels
  * Merges predicted parcel DF with violation dataframe on "unique" column (parcel_id || validation date)
  * Output is a list of model df's with parcel id, lat, long, TP dummy, Inspection Dummy. 

`mapping_models.ipynb`: This notebook simply takes the output of `run.py` and iterates through the list of 
selected model dataframes, converting each to a GeoDataFrame, and clustering by whether a parcel is a True 
Postive or False Positive.
  



 
