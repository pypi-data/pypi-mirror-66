import pandas as pd
import numpy as np
import math
from scipy.stats import rankdata

def rank_data(data_filename,list_of_weights,list_of_impacts):
	input_data_file=pd.read_csv(data_filename)
	X=input_data_file.to_numpy()
	Y=input_data_file
	X=X[:,1:]
	if len(list_of_weights)!=np.size(X,axis=1):
		raise ValueError('Number of entries in weights does not match the number of attributes in the dataset')
	if len(list_of_impacts)!=np.size(X,axis=1):
		raise ValueError('Number of entries in impacts does not match the number of attributes in the dataset')
	if '0' in list_of_weights:
		raise ValueError('0 cannot be entered as a weight')
	ssq=np.sum(X**2,axis=0)
	root_ssq=[]
	for i in range(len(ssq)):
		root_ssq.append(math.sqrt(ssq[i]))

	np.asarray(list_of_weights)
	list_of_weights=np.float_(list_of_weights)

	X=np.divide(X,root_ssq)

	X=np.multiply(X,list_of_weights)

	max_values=np.amax(X,axis=0)
	min_values=np.amin(X,axis=0)
	ideal_worst=[]
	ideal_best=[]

	for i in range(len(list_of_impacts)):
		if list_of_impacts[i]=='+':
			ideal_best.append(max_values[i])
			ideal_worst.append(min_values[i])
		else:
			ideal_best.append(min_values[i])
			ideal_worst.append(max_values[i])

	s_plus=[]

	for i in range(np.size(X,axis=0)):
	    s_plus.append(np.sqrt(np.sum((np.subtract(X[i,:],ideal_best))**2)))
	s_minus=[]

	for i in range(np.size(X,axis=0)):

		s_minus.append(np.sqrt(np.sum((np.subtract(X[i,:],ideal_worst))**2)))

	sum_s_plus_s_minus=np.add(s_plus,s_minus)
	performance_score=np.divide(s_minus,sum_s_plus_s_minus)
	rank=rankdata(performance_score)
	final_rank=len(rank)+1-rank
	final_rank=list(final_rank)
	final_rank=[int(i) for i in final_rank]
	Y=Y.iloc[:,0]
	Y=list(Y)
	Y=pd.DataFrame({"Item":Y,"Rank":final_rank},columns=["Item","Rank"])
	return Y
