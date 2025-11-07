import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random



def DFS(G, sommet, seen, tree):
    """
    DFS simple qui update tree en temps réel, et donc stock l'arbre dans tree.
    """
    seen.add(sommet)
    for i in list(G.successors(sommet)):
        if i not in seen : 
            tree.add((sommet,i))
            DFS(G, i, seen, tree)
    return

def Strong_Bridges(G, A, E_oriente):
    """
    calcul tous les strong bridges de G à l'aide de T+ et T-. On prend un sommet de G aléatoire.
    """
    E2 = set()
    for i in E_oriente:
        E2.add((A[i][0], A[i][1])) 
        
    sommet = random.randint(0, len(list(G.nodes()))-1) #on prend un sommet aléatoire commme racine et antiracine de T+ et T-.
    seen = set()
    T_plus = set()
    DFS(G, list(G.nodes())[sommet], seen,T_plus)

    seen = set()
    T_moins1 = set()
    G_inverse = G.reverse(copy=True)
    DFS(G_inverse, list(G.nodes())[sommet], seen, T_moins1)

    T_moins = set()
    for i,j in T_moins1:
        T_moins.add((j,i)) #on inverse T- car on a pris le graphe inverse.
    
    G_prime = set(list(T_moins)+list(T_plus)) #set car on ne veut pas de doublons
    strong_bridges = set()
    for u,v in G_prime : 
        if (u,v) in E2 :
            G.remove_edge(u,v)
            if not(nx.is_strongly_connected(G)) :
                strong_bridges.add((u,v))
            G.add_edge(u,v)
    return strong_bridges

def candidat_st(G, A, E_oriente):
    """
    renvoie les couples s,t pertinant. Ceux dont le plus court chemin passe par au moins une arête.
    """
    E2 = set()
    for i in E_oriente:
        E2.add((A[i][0], A[i][1]))
        
    candidat = []
    for source in G.nodes():
        paths = nx.single_source_dijkstra_path(G, source)
        for target, path in paths.items():
            if source != target:
                if any((path[k], path[k + 1]) in E2 for k in range(len(path) - 1)):
                    candidat.append((source, target))

    return candidat


def Update_Graphe(A, E, Strong_Bridge):

    A_update = [(u, v, w) for (u, v, w) in A if (v,u) not in Strong_Bridge]

    
    triplet_dict = {}
    for idx, (u, v, w) in enumerate(A_update):
        triplet_dict[(u, v)] = idx

    visited = set()
    E_update = []
    for (u, v, w) in A_update:
        if (v, u) in triplet_dict:
            idx1 = triplet_dict[(u, v)]
            idx2 = triplet_dict[(v, u)]
            
            if idx1 not in visited and idx2 not in visited:
                E_update.extend([idx1, idx2])
                visited.add(idx1)
                visited.add(idx2)
    E_update = [i for i in E_update if A_update[i] in [A[j] for j in E]] #On ne veut que des anciennes aretes de E
    Graphe_update = nx.DiGraph()
    Graphe_update.add_weighted_edges_from(A_update)
    return A_update, E_update, Graphe_update