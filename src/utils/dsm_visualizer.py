import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src.models.ontology import Ontology

def generate_dsm(ontology: Ontology, save_path: str = None):
    """
    Generate Design Structure Matrix from ontology.
    
    Args:
        ontology: Ontology object
        save_path: Optional path to save visualization
    
    Returns:
        Adjacency matrix (numpy array)
    """
    G = ontology.to_networkx()
    nodes = list(G.nodes())
    
    # Build adjacency matrix
    n = len(nodes)
    matrix = np.zeros((n, n))
    
    for i, node_i in enumerate(nodes):
        for j, node_j in enumerate(nodes):
            if G.has_edge(node_i, node_j):
                matrix[i, j] = 1
    
    # Visualize
    fig, ax = plt.subplots(figsize=(12, 10))
    
    sns.heatmap(
        matrix,
        xticklabels=[G.nodes[n]['name'][:20] for n in nodes],
        yticklabels=[G.nodes[n]['name'][:20] for n in nodes],
        cmap="Blues",
        cbar=False,
        square=True,
        linewidths=0.5,
        ax=ax
    )
    
    plt.title(f"Design Structure Matrix: {ontology.reactor}", fontsize=16)
    plt.xlabel("Depends On →", fontsize=12)
    plt.ylabel("Component ↓", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=200, bbox_inches='tight')
        print(f"✅ DSM saved to {save_path}")
    
    plt.show()
    
    return matrix

# Usage:
# from src.models.ontology import Ontology
# ontology = Ontology.load("data/ontologies/marvel_ontology.json")
# matrix = generate_dsm(ontology, save_path="data/marvel_dsm.png")