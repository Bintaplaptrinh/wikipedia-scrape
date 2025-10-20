import os
from bfs.bfs_pathfinder import BFSPathfinder
from analytic.q4 import InfluenceAnalyzer
from analytic.q5 import Correlation
from scrape.scrape_wiki import CountryScrape
from load_data import load_countries


def main():
    #load contries data
    countries = load_countries()
    
    if not countries:
        print("error: no contries loaded")
        return
    
    #build graph
    scape = CountryScrape()
    scape.load_countries()
    print(f"loaded {len(scape.country_set)} countries")
    
    #threads scrape
    scape.build_graph()
    scape.save_graph()
    #scrape done
    
    #bfs
    bfs = BFSPathfinder()
    path, distance = bfs.bfs('Viet Nam', 'France')
    
    if path:
        print(f"Path: {'->'.join(path)}")
        print(f"Distance: {distance}")
    else:
        print("No path found between Viet Nam and France")
        
    #analyztic q4
    analyzer = InfluenceAnalyzer()
    results = analyzer.analyze_influen()
    analyzer.save_results(results)
    
    print("\nTop 10 Influential Countries:")
    print("Top 10 Countries by Degree Centrality:")
    for country, score in results['degree_centrality']:
        print(f"{country}: {score:.6f}")
        
    print("\nTop 10 Countries by PageRank:")
    for country, score in results['pagerank']:
        print(f"{country}: {score:.6f}")
        
    print("\nTop 10 Countries by Betweenness:")
    for country, score in results['betweenness']:
        print(f"{country}: {score:.6f}")
        
    #analytic q5
    corr_anal = Correlation()
    corr_anal.anal_pop_correlation()
    corr_anal.anal_density_corr()
    
    
    
    
        
if __name__ == '__main__':
    main()