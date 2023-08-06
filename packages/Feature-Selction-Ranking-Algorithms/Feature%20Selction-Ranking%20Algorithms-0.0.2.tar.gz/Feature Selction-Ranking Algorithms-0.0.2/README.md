#Feature Selection and Feature Ranking Algorithms :


A Python package that provides many feature selection and feature ranking algorithms

##Usage

Use the function call like :

``````
fsfr(dataset,fs = '...', fr = '...', ftf = '...')
``````

where :

"dataset" is the dataset to be passed which must be a :
	
	numerical valued datset (categorical, ordinal values are excluded) 
	The class variable (decisional attribute or variable) should be of numerical type


"fs" means feature selection method and is of the following types :

	gpso : Geometric Particle Swarm Optimisation
	ga : Genetic Alogorithm


"fr" means featuure ranking meand feature ranking and is of the following types :

	rsm_a : Rough Set Method 1
	rsm_b : Rough Set Method 2
	rsm_c : Rough Set Method 3
	mifsnd : Mutual Information Feature Selection-ND
	mrmr : Minimum Redundancy Maximum Relevance


If "fs" is used then, it is mandatory to specify the value of "ftf"
"ftf" means fitness function which takes values :

	ftf_1 : fitness function = 0.75 * (100/accuracy) + 0.25 * (no of features)
	ftf_2 : fitness function = 0.75 * accuracy + 0.25 * (1 / no of features)
	ftf_3 : fitness_function = accuracy * (1 - no of features/total no of features)

no of features= no of features taht are selected by the algorithm at that point

The feature selection and ranking can be used independently of each other by mentioning either fs='' or fr='' but both cannot be '' 
and it is preferable to use both at the same time in case of larger datasets.

Refrences for algorithms :

gpso with ftf_1 : https://www.researchgate.net/publication/4307926_Gene_selection_in_cancer_

rsm_a : http://library.isical.ac.in:8080/jspui/bitstream/10263/5158/1/Rough%20Sets%20for%20Selection%20of%20Molecular%20Descriptors%20to%20Predict%20Biological%20Activity%20of%20Molecules-IEEETOSMAC-%20Part%20C-AAR-40-6-2010-p%20639-648.pdf

rsm_b : https://ieeexplore.ieee.org/document/7104131 

mifsnd : https://www.sciencedirect.com/science/article/pii/S0957417414002164

The rest of the algorithms have been self developed and do not contain any materials from any other sources
