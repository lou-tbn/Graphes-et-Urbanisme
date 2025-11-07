import networkx as nx
import osmnx as ox
import json

def generate_graph_from_place(query):
    """
    Génère un graphe orienté depuis un lieu donné en utilisant OSMnx,
    extrait la composante fortement connexe maximale et la retourne.
    """
    # Téléchargement du graphe routier dirigé à partir d'un nom de lieu
    raw_graph = ox.graph_from_place(query, network_type="drive")

    # Création d'un graphe orienté (poids = longueur des routes)
    directed_graph = nx.DiGraph()
    for u, v, data in raw_graph.edges(data=True):
        weight = data.get("length", 1)
        if directed_graph.has_edge(u, v):
            # On garde le poids minimal si plusieurs arêtes existent entre deux nœuds
            directed_graph[u][v]["weight"] = min(directed_graph[u][v]["weight"], weight)
        else:
            directed_graph.add_edge(u, v, weight=weight)

    # Transfert des métadonnées depuis le graphe OSM d'origine pour un affichage du graphe dans le futur
    transfer_metadata(raw_graph, directed_graph)

    # Extraction de la plus grande composante fortement connexe
    largest_scc_graph = extract_largest_strongly_connected_component(directed_graph)

    data = nx.node_link_data(largest_scc_graph, edges="links")  # convertit en dictionnaire JSON compatible


    nom_fichier = f"Instances/{query}" # On peut changer le nom du fichier ici en remplacant query par le nouveau nom
    
    with open(nom_fichier, 'w') as f:
        json.dump(data, f)


def transfer_metadata(source_graph, target_graph):
    """
    Transfère les métadonnées (attributs de graphe et de nœuds)
    depuis le graphe OSM vers le graphe orienté.
    """
    target_graph.graph.update(source_graph.graph)
    for node in target_graph.nodes:
        if node in source_graph.nodes:
            target_graph.nodes[node].update(source_graph.nodes[node])


def extract_largest_strongly_connected_component(graph):
    """
    Supprime tous les nœuds qui ne sont pas dans la plus grande composante fortement connexe.
    Retourne un nouveau graphe avec uniquement cette composante.
    """
    # Recherche de toutes les composantes fortement connexes
    largest_component = set()
    nodes_to_remove = []

    for component in nx.strongly_connected_components(graph):
        if len(component) > len(largest_component):
            nodes_to_remove.extend(largest_component)
            largest_component = component
        else:
            nodes_to_remove.extend(component)

    # Création d'une copie du graphe sans les nœuds à supprimer
    graph_scc = graph.copy()
    graph_scc.remove_nodes_from(nodes_to_remove)

    return graph_scc

def path_and_edges(G):
    A = [(u, v, data.get('weight', 1)) for u, v, data in G.edges(data=True)]
    st = [(x,y) for x in G.nodes for y in G.nodes if x!=y]
    V = list(G.nodes)

    triplet_dict = {}
    for idx, (u, v, d) in enumerate(A):
        triplet_dict[(u, v)] = idx
        
    E = []
    visited = set()

    for idx1, (u, v, d) in enumerate(A):
        if (v, u) in triplet_dict:
            idx2 = triplet_dict[(v, u)]
            if idx1 != idx2 and idx1 not in visited and idx2 not in visited:
                E.extend([idx1, idx2])
                visited.add(idx1)
                visited.add(idx2)


    temp = []
    for (a,b) in nx.bridges(G.to_undirected()):
        for ((u,v,_),j) in [(A[k],k) for k in E]:
            if (u==a and v==b) or (u==b and v == a):
                temp.append(j)

    for i in temp:
        E.remove(i)

    return A,st,E,V

def import_instance(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return nx.node_link_graph(data, edges="links")

