#Q4: Quốc gia nào có "tầm ảnh hưởng thông tin" lớn nhất?

import networkx as nx
import json
class InfluenceAnalyzer:

    def __init__(self, file='./graph.json'):
        with open(file, 'r', encoding='utf-8') as f:
            g_dict = json.load(f)
            
        #convert to networkx digraph
        self.G = nx.DiGraph()
        
        for node, nei in g_dict.items():
            for n in nei:
                self.G.add_edge(node, n)

    def calculate_degree_centrality(self):
        in_deg = nx.in_degree_centrality(self.G)
        out_deg = nx.out_degree_centrality(self.G)
        #combine score
        combine = {node: in_deg[node] + out_deg[node] for node in self.G.nodes()}
        
        No10 = sorted(combine.items(), key=lambda x: x[1], reverse=True)[:10]
        return No10
    
    def calculate_pagerank(self):
        #networkx
        pagerank  = nx.pagerank(self.G, alpha=0.85)
        
        No10 = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:10]
        return No10
    
    def calculate_betweenness(self):
        between = nx.betweenness_centrality(self.G)
        
        No10 = sorted(between.items(), key=lambda x: x[1], reverse=True)[:10]
        return No10
    
    def analyze_influen(self):
        deg_cen = self.calculate_degree_centrality()
        pagerank = self.calculate_pagerank()
        between  = self.calculate_betweenness()
        
        return {
            'degree_centrality': deg_cen,
            'pagerank': pagerank,
            'betweenness': between
        }
        
        #save results
    def save_results(self, results, filepath='./influence_results.json'):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
            
if __name__ == '__main__':
    analyzer = InfluenceAnalyzer()
    results = analyzer.analyze_influen()
    analyzer.save_results(results)

    print("Influence analysis results saved to ./influence_results.json")

    print("Top 10 Countries by Degree Centrality:")
    for country, score in results['degree_centrality']:
        print(f"{country}: {score:.6f}")
        
    print("\nTop 10 Countries by PageRank:")
    for country, score in results['pagerank']:
        print(f"{country}: {score:.6f}")
