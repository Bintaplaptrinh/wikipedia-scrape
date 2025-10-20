#Q5: Có mối tương quan nào giữa dân số/kinh tế và "mức độ kết nối"?


import json
import numpy as np
import plotly.graph_objects as go
from scipy.stats import pearsonr, spearmanr


class Correlation:
    def __init__(self, contry_file='./countries.jsonl', graph_file='./graph.json'):
        with open(contry_file, 'r', encoding='utf-8') as f:
            self.countries = json.load(f)
        
        with open(graph_file, 'r', encoding='utf-8') as f:
            self.graph = json.load(f)
            
    def cal_connectivity(self):
        con = {}
        for country in self.countries:
            name = country.get('Country')
            out_deg = len(self.graph.get(name, []))
            
            in_deg = sum(1 for links in self.graph.values() if name in links)
            con[name] = {
                'out_degree': out_deg,
                'in_degree': in_deg,
                'total_degree': in_deg + out_deg
            }
        return con
            
    def anal_pop_correlation(self):
        con = self.cal_connectivity()
        
        pop = []
        deg = []
        
        for cn in self.countries:
            name = cn.get('Country')
            
            if name in con:
                pop.append(cn.get('poppulation'))
                deg.append(con[name]['total_degree'])
                
                
        #convert to numpy arr
        pop = np.array(pop, dtype=float)
        deg = np.array(deg, dtype=float)
        
        #cal correlation
        corr, p_value = pearsonr(pop, deg)
        print(f"pop vs connectivity:")
        print(f"Pearson correlation: {corr}")
        print(f"P-value: {p_value}")
        
        #plot
        self._plot_scatter(pop, deg, 'Population', 'Total Connectivity Degree', 'Population vs Connectivity')
        return corr, p_value
    
    
    def anal_density_corr(self):
        con = self.cal_connectivity()
        
        density = []
        deg = []
        
        for cn in self.countries:
            name = cn.get('Country')
            
            if name in con:
                density.append(cn['density'])
                deg.append(con[name]['total_degree'])
                
        #convert to numpy arr
        density = np.array(density, dtype=float)
        deg = np.array(deg, dtype=float)

        #cal correlation
        corr, p_value = spearmanr(density, deg)
        print(f"density vs connectivity:")
        print(f"Spearman correlation: {corr}")
        print(f"P-value: {p_value}")

        #plot
        self._plot_scatter(density, deg, 'Population Density', 'Total Connectivity Degree', 'Density vs Connectivity')
        return corr, p_value

    def _plot_scatter(self, x, y, xlabel, ylabel, title):
        fig = go.Figure(data=go.Scatter(
            x=x,
            y=y,
            mode='markers'
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title=xlabel,
            yaxis_title=ylabel
        )
        
        fig.show()
        
if __name__ == '__main__':
    corr_analyzer = Correlation()
    corr, p_value = corr_analyzer.anal_pop_correlation()
    corr2, p_value2 =corr_analyzer.anal_density_corr()
    
    print("Correlation analysis completed.")
    
    #pop vs connectivity sv
    print("Population vs Connectivity:")
    print(f"Pearson correlation: {corr}, P-value: {p_value}")
    
    #density vs connectivity sv
    print("Population Density vs Connectivity:")
    print(f"Spearman correlation: {corr2}, P-value: {p_value2}")
    