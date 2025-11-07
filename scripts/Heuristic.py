import random
import networkx as nx

def heuristic_pour_bridgless(G, E, sommet, E_oriente_prime, lemme2):
    """
    Oriente les arêtes d'un sous-graphe sans ponts pour maintenir une forte connexité.
    
    Paramètres :
    - G : sous-graphe sans ponts
    - E : ensemble d'arêtes bidirectionnelles initiales
    - sommet : sommet de départ pour le DFS
    - E_oriente_prime : liste des arêtes orientées résultantes (modifiée en place)
    - lemme2 : liste des arêtes critiques identifiées selon une condition particulière
    """
    low = [i for i in range(len(list(G.nodes())))]  # Valeurs low utilisées dans le DFS
    V = list(G.nodes())  # Liste des sommets du graphe
    adj = nx.to_numpy_array(G, dtype=int).tolist()  # Matrice d'adjacence (liste de listes)

    # Lance le DFS récursif
    if dfs_rec(adj, {sommet}, sommet, [], low, E, {}, V, E_oriente_prime, lemme2) == 0:
        return None
    return E_oriente_prime


def heuristic(G, A, E, seed):
    """
    Applique l'heuristique d'orientation sur les composantes fortement connexes sans ponts.
    
    Paramètres :
    - G : graphe de départ
    - E : indices des arêtes bidirectionnelles
    - seed : graine aléatoire
    
    Retour :
    - E_oriente_prime : liste des arêtes orientées
    - lemme2 : arêtes critiques orientées dans un certain cas particulier
    """
    random.seed(seed)
    E_couple = [A[i][:2] for i in E]
    G_oriente = G.copy()
    E_oriente_prime = []
    lemme2 = []

    # Découpe le graphe en sous-graphes sans ponts
    sccs = subGraph(G_oriente)
    
    for X in sccs:
        # Choisit un sommet de départ aléatoire pour le DFS
        sommet = random.randint(0, len(list(X.nodes())) - 1)
        heuristic_pour_bridgless(X, E_couple, sommet, E_oriente_prime, lemme2)
    
    return [i for i, (u_, v_, _) in enumerate(A) if (u_, v_) in E_oriente_prime]


def dfs_rec(adj, seen, sommet, tree, low, E, prefixe, V, E_oriente_prime, lemme2):
    """
    DFS modifié avec calcul des valeurs low pour orienter les arêtes en préservant la forte connexité.
    """
    prefixe[sommet] = len(prefixe)
    low[sommet] = len(prefixe) - 1

    # Exploration aléatoire des voisins
    for i in random_range(len(adj)):
        if adj[sommet][i] != 0 and i not in seen:
            seen.add(i)
            tree.append((sommet, i))
            if dfs_rec(adj, seen, i, tree, low, E, prefixe, V, E_oriente_prime, lemme2) == 0:
                return 0

    parent = -1
    for i in range(len(adj)):
        if adj[sommet][i] != 0 and (sommet, i) not in tree and (i, sommet) not in tree:
            # Arête de retour
            low[sommet] = min(low[sommet], low[i])
            if (V[sommet], V[i]) in E or (V[i], V[sommet]) in E:
                E_oriente_prime.append((V[sommet], V[i]))  # Orientation dans un sens arbitraire
                adj[i][sommet] = 0  # Supprime l'autre direction
        elif adj[i][sommet] != 0 and (i, sommet) in tree:
            parent = i

    # Traitement après visite des enfants
    if parent != -1:
        if low[sommet] < prefixe[sommet]:  # Arête de retour : mise à jour de low
            low[parent] = min(low[sommet], low[parent])
            if (V[sommet], V[parent]) in E or (V[parent], V[sommet]) in E:
                E_oriente_prime.append((V[parent], V[sommet]))
                adj[sommet][parent] = 0
        elif low[sommet] == prefixe[sommet]:  # Lemme 2 : cas spécial
            low[sommet] = low[parent]
            if (V[sommet], V[parent]) in E or (V[parent], V[sommet]) in E:
                E_oriente_prime.append((V[sommet], V[parent]))
                lemme2.append((V[sommet], V[parent]))
                adj[parent][sommet] = 0
            else:
                print("le graphe n'est pas orientable")
                return 0
    return 1


def subGraph(G):
    """
    Supprime les ponts du graphe et retourne ses composantes fortement connexes de taille > 1.
    """
    G_bridgless = G.copy()
    for (u, v) in nx.bridges(G.to_undirected()):
        G_bridgless.remove_edge(u, v)
        G_bridgless.remove_edge(v, u)  # Supprime l'arête dans les deux sens
    sccs = nx.strongly_connected_components(G_bridgless)
    return [G_bridgless.subgraph(c).copy() for c in sccs if len(list(c)) > 1]


def random_range(n):
    """
    Retourne une liste aléatoire des indices de 0 à n-1.
    """
    l = list(range(n))
    random.shuffle(l)
    return l
