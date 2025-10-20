import plotly.graph_objects as go
import json
import networkx as nx


def vis_top_country(graph_file='./graph.json', top_n=10):
    with open(graph_file, 'r', encoding='utf-8') as f:
        g_dict = json.load(f)
        
    G = nx.DiGraph()
    
    for node, nei in g_dict.items():
        for n in nei:
            G.add_edge(node, n)
            
    degree_cen = nx.degree_centrality(G)
    top_countries = sorted(degree_cen.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    countries, scores = zip(*top_countries)
    
    fig = go.Figure(data=[go.Bar(x=countries, y=scores)])
    fig.update_layout(
        title=f'Top {top_n} Countries by Degree Centrality',
        xaxis_title='Country',
        yaxis_title='Degree Centrality Score'
    )
    
    fig.show()
    
def vis_path(path):
    
    G = nx.DiGraph()
    for i in range(len(path) - 1):
        G.add_edge(path[i], path[i + 1])
        
    pos = nx.spring_layout(G)
    
    nx.draw(G, pos, with_labels=True, node_color='lightblue', arrows=True)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    import matplotlib.pyplot as plt
    plt.title('Path Visualization')
    plt.show()
