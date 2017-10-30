##Select models to utilize for analysis 

## Cincinnati project



import os 

import pandas as pd

import numpy as np 

import sklearn

from sklearn.decomposition import PCA as sklearnPCA

from sklearn.metrics import mean_squared_error as mse

from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt

import matplotlib.mlab as mlab

import re 

from datetime import datetime

from datetime import timedelta

import calendar

from sklearn import preprocessing

from sklearn import datasets,tree

from IPython.display import Image 

from sklearn.tree import DecisionTreeRegressor

import pickle

from itertools import *

from scipy.stats import spearmanr





def create_weights(weights, length = 5):

	'''

	Creates weights that add to 1 



	Returns: A list of weights

	'''

    perms = list(product(weights, repeat = length))

    weight_list = list(filter(lambda x: sum(x)==1, perms))



    return weight_list





def normalize_data(data, variable, more_is_better = True):

	'''

	Normalize data from 0 to 100



	'''

	if more_is_better:

		data["norm" + variable] = (data[variable] - min(data[variable])) / (max(data[variable]) - 

                                                             min(data[variable]))

	else:

		data["norm" + variable] = (max(data[variable]) - 

                           data[variable]) / (max(data[variable]) - min(data[variable]))





def create_scores(data, variables_interest, weight_list):

	'''

	Creates scores given variable of interests and a list of weights. 



	Returns: A data with scores 

	'''

	for weight in weight_list:

		pass



def create_scores_hard_code(data, dates_list, weights, selected_weights = None):

	'''

	Creates scores given variable of interests and a list of weights. 



	Returns: A data with scores 

	'''

	

	for date in dates_list:

		   

	    data_f = data[data.validation_date == validation_date]

	    sum1 = create_weights(weights)



	    feat = ["score_violation", "score||prec_at_1", "score||prec_at_5", 

	                         "score||prec_at_10", "score||prec_at_20"]



	    

	    corr_data = pd.DataFrame()

	    corr_data["model_id"] = data_f.model_id

	    for i, comb in enumerate(sum1):

	        corr_data[str(comb)] = comb[0]*data_f[feat[0]] + comb[1]*data_f[feat[1]] + comb[2]*data_f[feat[2]] + \

	                                comb[3]*data_f[feat[3]] + comb[4]*data_f[feat[4]]



	    

	    if selected_weights == None:

	    	selected_weights = ['(1, 0, 0, 0, 0)', '(0, 1, 0, 0, 0)', '(0, 0, 1, 0, 0)', '(0, 0, 0, 0, 1)',

                  '(0.6, 0.4, 0, 0, 0)', '(0.6, 0, 0.4, 0, 0)', '(0.6, 0, 0, 0.4, 0)', 

                  '(0.6, 0, 0, 0, 0.4)', '(0, 0.6, 0.4, 0, 0)', 

                  '(0, 0, 0.6, 0.4, 0)', '(0, 0, 0, 0.6, 0.4)', '(0.2, 0.2, 0.2, 0.2, 0.2)']



	    for score in selected_weights:

	        row = corr_data.sort_values( by = score, 

	                          ascending = False).head(1)[["model_id",

	                                                     score]]



	        row["weights"] = score

	        row["key"] = '["score_violation", "score||prec_at_1", "score||prec_at_5", \

	                         "score||prec_at_10", "score||prec_at_20"]'

	        row["date"] = date

	        row = row.rename(columns={score: 'score'})

	        model_scores = model_scores.append(row, ignore_index = True)





	    with open('corr_data', 'wb') as fp:

			pickle.dump(corr_data, fp)



	return model_scores



if __name__ == '__main__':



	data = pd.read_csv("final_output.csv")

	

	models = pd.read_csv("output_csv.csv")



	data = data.merge(models, left_on = "model_id", right_on = "||_id")



	weights = [0,.2,.4,.6,.8,1]



	dates_list = list(data.validation_date.unique())

	model_scores = pd.DataFrame()



	model_scores = create_scores_hard_code(data, dates_list, weights, selected_weights = None)

	model_scores.to_csv(sys.argv[1])





	


