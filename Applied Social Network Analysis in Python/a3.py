'''
In this assignment you will explore measures of centrality on two networks, a friendship network in Part 1, and a blog network in Part 2.
'''
import networkx as nx
import sys, os



sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



__author__ = 'Chris Hilldrup'



# NOTE: following provided by Coursera
G1 = nx.read_gml(sys.path[-1] + '/Data/friendships.gml')
'''
Part 1

Answer questions 1-4 using the network G1, a network of friendships at a university department. Each node corresponds to a person, and an edge indicates friendship.

The network has been loaded as networkx graph object G1.
'''



'''
Find the degree centrality, closeness centrality, and normalized betweeness centrality (excluding endpoints) of node 100.

This function should return a tuple of floats (degree_centrality, closeness_centrality, betweenness_centrality).
'''
def answer_one():
    degree_cen = nx.degree_centrality(G1)[100]
    close_cen = nx.closeness_centrality(G1)[100]
    between_cen = nx.betweenness_centrality(G1)[100]
    
    return degree_cen, close_cen, between_cen



'''
For Questions 2, 3, and 4, assume that you do not know anything about the structure of the network, except for the all the centrality values of the nodes. That is, use one of the covered centrality measures to rank the nodes and find the most appropriate candidate.¶
'''



'''
Suppose you are employed by an online shopping website and are tasked with selecting one user in network G1 to send an online shopping voucher to. We expect that the user who receives the voucher will send it to their friends in the network. You want the voucher to reach as many nodes as possible. The voucher can be forwarded to multiple users at the same time, but the travel distance of the voucher is limited to one step, which means if the voucher travels more than one step in this network, it is no longer valid. Apply your knowledge in network centrality to select the best candidate for the voucher.

This function should return an integer, the name of the node.
'''
def answer_two():
    degree_cen = nx.degree_centrality(G1)
    node = max(zip(degree_cen.values(), degree_cen.keys()))
    
    return node[1]



'''
Now the limit of the voucher’s travel distance has been removed. Because the network is connected, regardless of who you pick, every node in the network will eventually receive the voucher. However, we now want to ensure that the voucher reaches the nodes in the lowest average number of hops.

How would you change your selection strategy? Write a function to tell us who is the best candidate in the network under this condition.

This function should return an integer, the name of the node.
'''
def answer_three():
    close_cen = nx.closeness_centrality(G1)
    node = max(zip(close_cen.values(), close_cen.keys()))
            
    return node[1]



'''
Assume the restriction on the voucher’s travel distance is still removed, but now a competitor has developed a strategy to remove a person from the network in order to disrupt the distribution of your company’s voucher. Your competitor is specifically targeting people who are often bridges of information flow between other pairs of people. Identify the single riskiest person to be removed under your competitor’s strategy?

This function should return an integer, the name of the node.
'''
def answer_four():
    between_cen = nx.betweenness_centrality(G1)
    node = max(zip(between_cen.values(), between_cen.keys()))
    
    return node[1]



# NOTE: following provided by Coursera
G2 = nx.read_gml(sys.path[-1] + '/Data/blogs.gml')
'''
Part 2

G2 is a directed network of political blogs, where nodes correspond to a blog and edges correspond to links between blogs. Use your knowledge of PageRank and HITS to answer Questions 5-9.
'''



'''
Apply the Scaled Page Rank Algorithm to this network. Find the Page Rank of node 'realclearpolitics.com' with damping value 0.85.

This function should return a float.
'''
def answer_five():
    G2_pagerank = nx.pagerank(G2)
    
    return G2_pagerank['realclearpolitics.com']



'''
Apply the Scaled Page Rank Algorithm to this network with damping value 0.85. Find the 5 nodes with highest Page Rank.

This function should return a list of the top 5 blogs in desending order of Page Rank.
'''
def answer_six():
    G2_pagerank = nx.pagerank(G2)
    pagerank_top5 = sorted(G2_pagerank, key=lambda x: G2_pagerank[x], reverse=True)
    
    return pagerank_top5[:5]



'''
Apply the HITS Algorithm to the network to find the hub and authority scores of node 'realclearpolitics.com'.

Your result should return a tuple of floats (hub_score, authority_score).
'''
def answer_seven():
    G2_hits_hub, G2_hits_auth = nx.hits(G2)
    
    return G2_hits_hub['realclearpolitics.com'], G2_hits_auth['realclearpolitics.com']



'''
Apply the HITS Algorithm to this network to find the 5 nodes with highest hub scores.

This function should return a list of the top 5 blogs in desending order of hub scores.
'''
def answer_eight():
    G2_hits_hub, _ = nx.hits(G2)
    hub_top5 = sorted(G2_hits_hub, key=lambda x: G2_hits_hub[x], reverse=True)
    
    return hub_top5[:5]



'''
Apply the HITS Algorithm to this network to find the 5 nodes with highest authority scores.

This function should return a list of the top 5 blogs in desending order of authority scores.
'''
def answer_nine():
    _, G2_hits_auth = nx.hits(G2)
    auth_top5 = sorted(G2_hits_auth, key=lambda x: G2_hits_auth[x], reverse=True)
    
    return auth_top5[:5]
