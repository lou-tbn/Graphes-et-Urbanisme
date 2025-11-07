import networkx as nx

def tabu(s0, it, maxTabuSize, fitness, getNeighbors, tabuTest, A, E):
    """
    Algorithme de recherche tabou pour trouver une orientation optimale.
    
    Paramètres :
    - s0 : solution initiale (indices dans E à garder dans le graphe orienté)
    - it : nombre maximal d'itérations
    - maxTabuSize : taille maximale de la liste taboue
    - fitness : fonction d'évaluation d'une solution
    - getNeighbors : fonction générant les voisins admissibles
    - tabuTest : fonction de test tabou
    - A : liste des arêtes pondérées [(u, v, weight), ...]
    - E : liste des indices des arêtes bidirectionnelles à gérer

    Retour :
    - sBest : meilleure solution trouvée
    - n : nombre d'itérations réalisées
    """

    # Regroupe les orientations d'arêtes par paires
    E_couple = [(E[i], E[i+1]) for i in range(0, len(E) - 1, 2)]  

    # Trie la solution initiale selon l'ordre des E_couple
    s0 = sorted(s0, key=lambda x: [y for t in E_couple for y in t].index(x))

    # Initialisation des variables
    sBest = s0          # Meilleure solution trouvée
    sCurr = s0          # Solution actuelle
    bestCandidate = s0  # Meilleur voisin admissible
    bestFitness = fitness(sBest, A, E)  # Score de la solution initiale
    
    tabuList = []       # Liste taboue (historique des inversions récentes)
    n = 0               # Compteur d’itérations

    while n < it:
        # Génère les voisins de la solution actuelle
        sNeighborhood = getNeighbors(sCurr, A, E_couple, E)

        bestCandidateFitness = float('inf')  # Score du meilleur voisin

        # Recherche du meilleur voisin non tabou
        for sCandidate in sNeighborhood:
            if tabuTest(sCandidate[1], tabuList):  # Vérifie si l’inversion est autorisée
                sCandidateFitness = fitness(sCandidate[0], A, E)
                if sCandidateFitness < bestCandidateFitness:
                    bestCandidate = sCandidate[0]
                    bestCandidateInv = sCandidate[2]  # Inversion appliquée
                    bestCandidateFitness = sCandidateFitness

        if bestCandidateFitness == float('inf'):
            break  # Aucun voisin valide trouvé

        # Mise à jour de la solution actuelle
        sCurr = bestCandidate  

        # Mise à jour de la meilleure solution trouvée
        if bestCandidateFitness < bestFitness:
            sBest = bestCandidate
            bestFitness = bestCandidateFitness

        # Ajout de l’inversion dans la liste taboue
        tabuList.append(bestCandidateInv)
        if len(tabuList) > maxTabuSize:
            tabuList.pop(0)  

        n += 1  # Incrémentation de l’itération
        
    return sBest, n


def tabuTest(sCandidate_direction, tabuList):
    """
    Vérifie si un changement de direction est autorisé selon la liste taboue.
    - Retourne False si l'inversion a déjà été effectuée récemment.
    """
    if sCandidate_direction in tabuList:
        return False
    if len(sCandidate_direction) == 1:
        # Cas d’une seule arête inversée
        return all(sCandidate_direction[0] not in t for t in tabuList)
    # Cas de deux arêtes : aucune ne doit apparaître dans la liste taboue
    return all(sCandidate_direction[0] not in t and sCandidate_direction[1] not in t for t in tabuList)


def fitness(sCandidate, A, E):
    """
    Évalue une solution en calculant la moyenne des longueurs des plus courts chemins
    dans le graphe orienté résultant.
    """
    sCandidate_set = set(sCandidate)
    E_set = set(E)

    # Construit le graphe orienté à partir de la solution
    A_orient = [
        edge for idx, edge in enumerate(A)
        if idx not in E_set or idx in sCandidate_set
    ]
    G = nx.DiGraph()
    G.add_weighted_edges_from(A_orient)

    # Renvoie la moyenne des longueurs de plus courts chemins pondérés
    return nx.average_shortest_path_length(G, weight='weight')


def getNeighbors(sCurr, A, E_couple, E):
    """
    Génère les voisins d'une solution en inversant une ou deux arêtes orientées,
    tout en s'assurant que le graphe reste fortement connexe.
    """
    sNeighborhood = []

    for i in range(len(E_couple)):
        # Cas 1 : inverser une seule arête
        temp = sCurr.copy()
        temp[i] = E_couple[i][sCurr[i] == E_couple[i][0]]  # Inverse l'arête i
        A_orient = [v for v in A if A.index(v) not in E or A.index(v) in temp]
        G = nx.DiGraph()
        G.add_weighted_edges_from(A_orient)
        if nx.is_strongly_connected(G):
            sNeighborhood.append((temp, [temp[i]], [sCurr[i]]))

        # Cas 2 : inverser deux arêtes (i et j)
        for j in range(i + 1, len(E_couple)):
            temp = sCurr.copy()
            temp[i] = E_couple[i][sCurr[i] == E_couple[i][0]]
            temp[j] = E_couple[j][sCurr[j] == E_couple[j][0]]
            A_orient = [v for v in A if A.index(v) not in E or A.index(v) in temp]
            G = nx.DiGraph()
            G.add_weighted_edges_from(A_orient)
            if nx.is_strongly_connected(G):
                sNeighborhood.append((temp, [temp[i], temp[j]], [sCurr[i], sCurr[j]]))

    return sNeighborhood
