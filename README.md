# Applied-Data-Science-with-Python


###### About This Specialization (taken from Coursera description)

The 5 courses in this University of Michigan specialization introduce learners to data science through the python programming language. This skills-based specialization is intended for learners who have a basic python or programming background, and want to apply statistical, machine learning, information visualization, text analysis, and social network analysis techniques through popular python toolkits such as pandas, matplotlib, scikit-learn, nltk, and networkx to gain insight into their data.


###### Modules Used:

- Pandas
- Numpy
- Matplotlib
- Scikit-learn
- Nltk
- Networkx
- Gensim (LdaModel)
- Scipy.stats (ttest_ind)



## Introduction to Data Science in Python


###### About This Course (taken from Coursera description):

This course will introduce the learner to the basics of the python programming environment, including fundamental python programming techniques such as lambdas, reading and manipulating csv files, and the numpy library. The course will introduce data manipulation and cleaning techniques using the popular python pandas data science library and introduce the abstraction of the Series and DataFrame as the central data structures for data analysis, along with tutorials on how to use functions such as groupby, merge, and pivot tables effectively. By the end of this course, students will be able to take tabular data, clean it, manipulate it, and run basic inferential statistical analyses.


###### a1.py

Introduction to Pandas dataframe, and answer basic statistical questions about data from 'olympics.csv' and 'census.csv'.


###### a2.py

Perform a union merge of country data from 'Energy Indicators.xls', 'world_bank.csv', and 'scimagojr-3.xlsx'. Answer questions concerning the top 15 countries by gdp over a ten year period.


###### a3.py

Using data from 'gdplev.xls' and 'City_Zhvi_AllHomes.csv', perform a ttest comparing the home values of university towns to non-university towns.



## Applied Plotting, Charting & Data Representation in Python


###### About This Course (taken from Coursera description):

This course will introduce the learner to information visualization basics, with a focus on reporting and charting using the matplotlib library. The course will start with a design and information literacy perspective, touching on what makes a good and bad visualization, and what statistical measures translate into in terms of visualizations. The second week will focus on the technology used to make visualizations in python, matplotlib, and introduce users to best practices when creating basic charts and how to realize design decisions in the framework. The third week will be a tutorial of functionality available in matplotlib, and demonstrate a variety of basic statistical charts helping learners to identify when a particular method is good for a particular problem. The course will end with a discussion of other forms of structuring and visualizing data. 


###### a1.py

Using the NOAA data set 'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv', plot line graphs of the min and max temperatures for 2005-2014, and shade the area between them. Then overlay a scatter plot of days in 2015 that exceeded these previous min and maxes.

Result saved as a1_result.png


###### a2.py

Plot bar graphs based on four sets of random numpy arrays. Implemented a color bar that describes whether or not a bar graph's data is included in the desired y-axis value. Desired y-axis can be changed by clicking.

Result saved as a2_result.png


###### a3.py

Self directed assignment. Plotted crop yield vs delta temperature change from previous year. Regions plotted include the world, and economic country groups according to UN M49 (2009). Data obtained from www.fao.org/faostat. Data files used: 'Environment_Temperature_change_E_All_Data_(Normalized).zip' and 'Production_Crops_E_All_Data_(Normalized).zip'.

Result saved as a3_result.png


## Applied Machine Learning in Python


###### About This Course (taken from Coursera description):


This course will introduce the learner to applied machine learning, focusing more on the techniques and methods than on the statistics behind these methods. The course will start with a discussion of how machine learning is different than descriptive statistics, and introduce the scikit learn toolkit through a tutorial. The issue of dimensionality of data will be discussed, and the task of clustering data, as well as evaluating those clusters, will be tackled. Supervised approaches for creating predictive models will be described, and learners will be able to apply the scikit learn predictive modelling methods while understanding process issues related to data generalizability (e.g. cross validation, overfitting). The course will end with a look at more advanced techniques, such as building ensembles, and practical limitations of predictive models. By the end of this course, students will be able to identify the difference between a supervised (classification) and unsupervised (clustering) technique, identify which technique they need to apply for a particular dataset and need, engineer features to meet that need, and write python code to carry out an analysis. 


###### a1.py

Introduction to K-nearest neighbor classifier using Breast Cancer Wisconsin (Diagnostic) Database in scikit-learn. Used classifier to identify potentially malignant tumors.


###### a2.py

Explored performance between model complexity and generalization. Models used were linear regression models using polynomial features ranging from 0 to 9 degrees, decistion tree classifier, and support vector classifier.


###### a3.py

Using 'fraud_data.csv', train several support vector, and logistic regression classifiers with varying parameters, and evaluate ability to detect fraud.


###### a4.py

Create, and train a model on 'train.csv', and predict compliance for entries in 'test.csv'. Training and test data come from the Detroit Open Data Portal regarding blight ticket compliance.



## Applied Text Mining in Python


###### About This Course (taken from Coursera description):

This course will introduce the learner to text mining and text manipulation basics. The course begins with an understanding of how text is handled by python, the structure of text both to the machine and to humans, and an overview of the nltk framework for manipulating text. The second week focuses on common manipulation needs, including regular expressions (searching for text), cleaning text, and preparing text for use by machine learning processes. The third week will apply basic natural language processing methods to text, and demonstrate how text classification is accomplished. The final week will explore more advanced methods for detecting the topics in documents and grouping them by similarity (topic modelling). 


###### a1.py

Extract all dates of varying formats from 'dates.txt', and sort them.


###### a2.py

Explore Moby Dick ('moby.txt') with nltk, and provide spelling corrections or three words based on Jaccard distance (trigram and 4-gram), and edit distance.


###### a3.py

Predict if a message is spam ('spam.csv') by fitting and transforming data using a count vectorizer and tf-idf vectorizer, then fit the vectorized data to multinomial Naive Bayes classifers. Compare results to predictions of support vector, and logistic regression classifiers after adding additional features: message length, digits per document, and number of non-word characters in message. 


###### a4.py

Determine document path similarity using nltk wordnets. Then using gensim's LdaModel find topic distributions of 'newgroups' and new_doc (in a4.py).



## Applied Social Network Analysis in Python


###### About This Course (taken from Coursera description):

This course will introduce the learner to network analysis through tutorials using the NetworkX library. The course begins with an understanding of what network analysis is and motivations for why we might model phenomena as networks. The second week introduces the concept of connectivity and network robustness. The third week will explore ways of measuring the importance or centrality of a node in a network. The final week will explore the evolution of networks over time and cover models of network generation and the link prediction problem. 


###### a1.py

Create a networkx bipartite graph using 'Employee_Movie_Choices.txt', and with 'Employee_Relationships.txt' find the pearson correlation between employee relationship scores and the number of movies they have in common.


###### a2.py

Create graphs from 'email_network.txt', which is an internal email communication network for a mid-sized manufacturing company, and find varying graph metrics.


###### a3.py

Determine centrality and link analysis metrics of the two networks 'friendships.gml', and 'blogs.gml'.


###### a4.py

NOTE: this assignment requires networkx version 1.11

Determine which graph generating algorithm created each of five possible graphs, use a scikit-learn classifier to find the missing management salary values for the network 'email_prediction.txt', and use a scikit-learn classifier to predict new connections between nodes in 'Future_Connections.csv' based on the 'email_prediction.txt' network.
