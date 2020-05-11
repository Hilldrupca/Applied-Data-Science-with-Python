'''
Eight employees at a small company were asked to choose 3 movies that they would most enjoy watching for the upcoming company movie night. These choices are stored in the file Employee_Movie_Choices.txt.

A second file, Employee_Relationships.txt, has data on the relationships between different coworkers.

The relationship score has value of -100 (Enemies) to +100 (Best Friends). A value of zero means the two employees haven't interacted or are indifferent.

Both files are tab delimited.
'''
import networkx as nx
import pandas as pd
import numpy as np
import sys, os
from networkx.algorithms import bipartite



sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



__author__ = 'Chris Hilldrup'



# NOTE: following variables provided by Coursera
# This is the set of employees
employees = set(['Pablo',
                 'Lee',
                 'Georgia',
                 'Vincent',
                 'Andy',
                 'Frida',
                 'Joan',
                 'Claude'])

# This is the set of movies
movies = set(['The Shawshank Redemption',
              'Forrest Gump',
              'The Matrix',
              'Anaconda',
              'The Social Network',
              'The Godfather',
              'Monty Python and the Holy Grail',
              'Snakes on a Plane',
              'Kung Fu Panda',
              'The Dark Knight',
              'Mean Girls'])



'''
Using NetworkX, load in the bipartite graph from Employee_Movie_Choices.txt and return that graph.

This function should return a networkx graph with 19 nodes and 24 edges
'''
def answer_one():
    G_df = pd.read_csv(sys.path[-1] + '/Data/Employee_Movie_Choices.txt',
                       sep='\t', header=None, skiprows=1,
                       names=['employees','movies'])
    
    G = nx.from_pandas_edgelist(G_df, 'employees', 'movies')
    return G



'''
Using the graph from the previous question, add nodes attributes named 'type' where movies have the value 'movie' and employees have the value 'employee' and return that graph.

This function should return a networkx graph with node attributes {'type': 'movie'} or {'type': 'employee'}
'''
def answer_two():
    G = answer_one()
    G.add_nodes_from(employees, bipartite=0, type='employee')
    G.add_nodes_from(movies, bipartite=1, type='movie')
    
    return G



'''
Find a weighted projection of the graph from answer_two which tells us how many movies different pairs of employees have in common.

This function should return a weighted projected graph.
'''
def answer_three():
    G = answer_two()
    
    return bipartite.weighted_projected_graph(G, employees)



'''
Suppose you'd like to find out if people that have a high relationship score also like the same types of movies.

Find the Pearson correlation ( using DataFrame.corr() ) between employee relationship scores and the number of movies they have in common. If two employees have no movies in common it should be treated as a 0, not a missing value, and should be included in the correlation calculation.

This function should return a float.
'''
def answer_four():
    G = answer_three()
    G_df = pd.read_csv(sys.path[-1] + '/Data/Employee_Relationships.txt',
                       sep='\t', names = ['source','target','Weight'])
    
    G_df['Common Movies'] = 0
    for x,y in G_df.groupby(['source','target']):
        if x in G.edges:
            G_df.loc[y.index,'Common Movies'] = G[x[0]][x[1]]['weight']
            
    corr = G_df[['Weight','Common Movies']].corr(method='pearson')

    return corr.at['Weight','Common Movies']
