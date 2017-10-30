### Model Exploration

## Cincinnati Project 



#Do a quick exploration of models 



import os 

import pandas as pd

import numpy as np 

import matplotlib.pyplot as plt

import matplotlib.mlab as mlab

from clean_data import * 





def prec_histogram(data, PRECISION_N = "1", variable = None, value = None):

	'''

	Graph histograms of precision at a given  level. 

	'''

	

	precision = "prec_at_" + PRECISION_N 



	mu = data[precision].mean()

	sigma = data[precision].std()



	fig = plt.figure()

	# the histogram of the data

	if variable != None:

		data = data[data[variable] = value]



	n, bins, patches = plt.hist( data[precision], 100, normed = True, facecolor='blue', alpha=0.75)



	# add a 'best fit' line

	y = mlab.normpdf( bins, mu, sigma)

	l = plt.plot(bins, y, 'r--', linewidth=1)



	plt.xlabel('Precision at '+ PRECISION_N)

	plt.ylabel("Frequency in thousands")

	plt.grid(True)



	if variable != None:

		name = variable + value + precision 

	else:

		name = precision



	fig.savefig( 'hist' + name + '.png', dpi=fig.dpi)





def charts_parameters(classifier, parameter, precision):

	'''

	Graph performance of models according to parameters 

	'''

	fig, ax = plt.subplots()

	ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling

	groups = data.groupby(classifier)

	for name, group in groups:

	    

	        ax.plot(group[parameter], group[precision], marker='o', linestyle='', ms=12, label=name)



	    	ax.legend()



			plt.xlabel(parameter + ' in ' + name)

			plt.ylabel('Precision')

	    

			fig.savefig('chart' + name + parameter + precision + '.png', dpi=fig.dpi)





 if __name__ == '__main__':

 	filename = sys.argv[1]

 	data = pd.read_csv(filename)



 	STATS = ["mean", "max", "min", "std"]

 	PREC = ["1", "5", "10", "20"]



	# Check the number of models and results by type of regressor

	results = data.groupby("regressor").agg({"regressor":['count'],"prec_at_1":STATS,

	                               "prec_at_5":STATS,"prec_at_10":STATS,

	                               "prec_at_20":STATS}).reset_index()



	results.to_csv("results_by_regressor.csv")





	# Graph the histograms of precision

	for precision in PREC:

		prec_histogram(data, precision)





	#Obtain list of parameters 

	with open ('list_parameters', 'rb') as fp:

    	list_parameters = pickle.load(fp)



    #Plot histograms of precision for parameters and save results in file 

    for parameter in list_parameters:

    	for value in list(data[parameter].unique()):

    		prec_histogram(data, variable = parameter, value = value)



    

    #Plot scatterplot for parameters 



	



	# Create file by parameters

	STAT = 

	for parameter in parsed_list:

	    model_param = data.groupby(["regressor",parameter]).agg({"regressor":['count'],"prec_at_1":[STATS],

	                               "prec_at_5":[STATS],"prec_at_10":[STATS]})

	    print(model_param)





	#Plot histogram of precision for features and save results in file 