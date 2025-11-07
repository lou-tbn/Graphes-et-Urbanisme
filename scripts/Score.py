import networkx as nx

def compute_value(A,E, E_oriente,P):
    G = Recreate_Graphe(A,E,E_oriente)
    return nx.average_shortest_path_length(G, weight="weight") * len(P)


def Recreate_Graphe(A, E, E_oriente): #crée un graphe à partir de E_oriente -> bonne solution
    G = nx.DiGraph()
    G.add_weighted_edges_from([v for v in A if A.index(v) not in E or A.index(v) in E_oriente]) 
    return G