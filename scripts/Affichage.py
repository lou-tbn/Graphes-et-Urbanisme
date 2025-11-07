import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx

def print_graphe(Graphe,titre):
    fig, ax = ox.plot_graph(
        nx.MultiGraph(Graphe),
        show=False,   # Ne pas afficher tout de suite
        close=False   # Ne pas fermer la figure
    )
    ax.set_title(titre, fontsize=15, color='red')
    plt.show()


def print_graphe_arete(Graphe, titre, A, E):
    aretes = set([A[i][:2] for i in E])  # ensemble pour accès rapide

    # Créer une MultiGraph compatible OSMnx
    G = nx.MultiGraph(Graphe)

    # Construire la liste des couleurs d’arêtes
    edge_colors = []
    for u, v, k in G.edges(keys=True):
        if (u, v) in aretes or (v, u) in aretes:
            edge_colors.append("#8D3131")
        else:
            edge_colors.append('#999999')  # gris clair par défaut

    # Affichage avec couleurs personnalisées
    fig, ax = ox.plot_graph(
        G,
        edge_color=edge_colors,
        edge_linewidth=2,
        show=False,
        close=False
    )
    ax.set_title(titre, fontsize=15, color='red')
    plt.show()


def print_graphe_Strong_Bridges(Graphe, titre, A, E, Strong_Bridges):
    aretes = set([A[i][:2] for i in E])  # ensemble pour accès rapide

    # Créer une MultiGraph compatible OSMnx
    G = nx.MultiGraph(Graphe)

    # Construire la liste des couleurs d’arêtes
    edge_colors = []
    for u, v, k in G.edges(keys=True):
        if (u, v) in Strong_Bridges or (v, u) in Strong_Bridges:
            edge_colors.append("#4B6635")
        elif (u, v) in aretes or (v, u) in aretes:
            edge_colors.append("#8D3131")
        else:
            edge_colors.append('#999999')  # gris clair par défaut

    # Affichage avec couleurs personnalisées
    fig, ax = ox.plot_graph(
        G,
        edge_color=edge_colors,
        edge_linewidth=2,
        show=False,
        close=False
    )
    ax.set_title(titre, fontsize=15, color='red')
    plt.show()