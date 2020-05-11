''' 
In this assignment you will go through the process of importing and analyzing an internal email communication network between employees of a mid-sized manufacturing company. Each node represents an employee and each directed edge between two nodes represents an individual email. The left node represents the sender and the right node represents the recipient.
'''
import networkx as nx
import sys,os



sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



__auther__ = 'Chris Hilldrup'



'''
Using networkx, load up the directed multigraph from email_network.txt. Make sure the node names are strings.

This function should return a directed multigraph networkx graph.
'''
def answer_one():
    G = nx.read_edgelist(sys.path[-1] + '/Data/email_network.txt',
                         create_using=nx.MultiDiGraph(), delimiter='\t',
                         data=[('Time', int)])
    
    return G



'''
How many employees and emails are represented in the graph from Question 1?

This function should return a tuple (#employees, #emails).
'''
def answer_two():
    G = answer_one()
    
    return G.number_of_nodes(), G.number_of_edges()



'''
Part 1. Assume that information in this company can only be exchanged through email.

When an employee sends an email to another employee, a communication channel has been created, allowing the sender to provide information to the receiver, but not vice versa.

Based on the emails sent in the data, is it possible for information to go from every employee to every other employee?

Part 2. Now assume that a communication channel established by an email allows information to be exchanged both ways.

Based on the emails sent in the data, is it possible for information to go from every employee to every other employee?

This function should return a tuple of bools (part1, part2).
'''
def answer_three():
    G = answer_one()
    G_strong_conn = nx.is_strongly_connected(G)
    
    G_2 = G.to_undirected()
    G_2_strong_conn = nx.is_connected(G_2)
    
    return G_strong_conn, G_2_strong_conn



'''
How many nodes are in the largest (in terms of nodes) weakly connected component?

This function should return an int.
'''
def answer_four():
    G = answer_one()
    weak_comp = nx.weakly_connected_components(G)
    
    largest_comp = {}
    for x in weak_comp:
        if len(largest_comp) < len(x):
            largest_comp = x
    
    return len(largest_comp)



'''
How many nodes are in the largest (in terms of nodes) strongly connected component?

This function should return an int
'''
def answer_five():
    G = answer_one()
    strong_comp = nx.strongly_connected_components(G)
    
    largest_comp = {}
    for x in strong_comp:
        if len(largest_comp) < len(x):
            largest_comp = x
    
    return len(largest_comp)



'''
Using the NetworkX function strongly_connected_component_subgraphs, find the subgraph of nodes in a largest strongly connected component. Call this graph G_sc.

This function should return a networkx MultiDiGraph named G_sc.
'''
def answer_six():
    G = answer_one()
    
    # strongly_connected_component_subgraphs() depricated in version 2.1
    # and removed in version 2.4
    # using workaround suggested in version 2.1 announcement
    largest_comp = {}
    for x in nx.strongly_connected_components(G):
        if len(largest_comp) < len(x):
            largest_comp = x
            
    G_sc = G.subgraph(largest_comp) 
    
    return G_sc



'''
What is the average distance between nodes in G_sc?

This function should return a float.
'''
def answer_seven():
    G_sc = answer_six()
    
    return nx.average_shortest_path_length(G_sc)



'''
What is the largest possible distance between two employees in G_sc?

This function should return an int.
'''
def answer_eight():
    G_sc = answer_six()
    
    return nx.diameter(G_sc)



'''
What is the set of nodes in G_sc with eccentricity equal to the diameter?

This function should return a set of the node(s).
'''
def answer_nine():
    G_sc = answer_six()
    ecc = answer_eight()
    G_ecc = nx.eccentricity(G_sc)
    ecc_eq_dia = []
    
    for x in G_ecc:
        if G_ecc[x] == ecc:
            ecc_eq_dia.append(x)
            
    return set(ecc_eq_dia)



'''
What is the set of node(s) in G_sc with eccentricity equal to the radius?

This function should return a set of the node(s).
'''
def answer_ten():
    G_sc = answer_six()
    rad = nx.radius(G_sc)
    G_ecc = nx.eccentricity(G_sc)
    ecc_eq_rad = []
    
    for x in G_ecc:
        if G_ecc[x] == rad:
            ecc_eq_rad.append(x)
            
    return set(ecc_eq_rad)



'''
Which node in G_sc is connected to the most other nodes by a shortest path of length equal to the diameter of G_sc?

How many nodes are connected to this node?

This function should return a tuple (name of node, number of satisfied connected nodes).
'''
def answer_eleven():
    G_sc = answer_six()
    dia = nx.diameter(G_sc)
    G_spl = nx.shortest_path_length(G_sc)
    spl_eq_dia = ('',0)
    
    for x in G_spl:
        count = list(x[1].values()).count(dia)
        if spl_eq_dia[1] < count:
            spl_eq_dia = (x[0], count)
            
    return spl_eq_dia



'''
Suppose you want to prevent communication from flowing to the node that you found in the previous question from any node in the center of G_sc, what is the smallest number of nodes you would need to remove from the graph (you're not allowed to remove the node from the previous question or the center nodes)?

This function should return an integer.
'''
def answer_twelve():
    G_sc = answer_six()
    G_sc_center = nx.center(G_sc)[0] # only contains one node
    isolate_node = answer_eleven()[0]
    
    # An edge between G_sc_center and isolation_node exists.
    # There is a check for such an edge in
    # ../lib/python3.8/site-packages/networkx/algorithms/connectivity/cuts.py line 286
    # This was added in version 2.0 of networkx
    # 
    # Autograder uses networkx version 1.11 which does not have this check.
    # Output accepting by autograder:  5
    return len(nx.minimum_node_cut(G_sc, G_sc_center, isolate_node))



'''
Construct an undirected graph G_un using G_sc (you can ignore the attributes).

This function should return a networkx Graph.
'''
def answer_thirteen():
    return nx.Graph(answer_six())



'''
What is the transitivity and average clustering coefficient of graph G_un?

This function should return a tuple (transitivity, avg clustering).
'''
def answer_fourteen():
    G_un = answer_thirteen()
    
    return nx.transitivity(G_un), nx.average_clustering(G_un)

