
from collections import deque
import json
class BFSPathfinder:
    
    def __init__(self, graph_file='./graph.json'):
        with open(graph_file, 'r', encoding='utf-8') as f:
            self.graph = json.load(f)
            
    def bfs(self, start, end):
        if start not in self.graph or end not in self.graph:
            return None, -1
        
        queue  = deque([start])
        
        visit = {start}
        
        parent = {start: None}
        
        while queue:
            cur = queue.popleft()
            
            if cur == end:
                path = self.reconstruct_path(parent, start, end)
                return path, len(path) - 1
            
            #expand neghbor
            for nei in self.graph.get(cur, []):
                if nei not in visit:
                    visit.add(nei)
                    parent[nei] = cur
                    queue.append(nei)
                    
        return None, -1
    
    def reconstruct_path(self, par, start, end):
        path = []
        cur = end
        while cur is not None:
            path.append(cur)
            cur = par[cur]
        path.reverse()
        return path
    
    def find_all_path(self, start, max_distance=3):
        if start not in self.graph:
            return {}
        
        queue = deque([(start, 0)])
        visit = {start}
        paths = {start: [start]}
        
        while queue:
            cur, dist = queue.popleft()
            
            if dist >= max_distance:
                continue
            
            for nei in self.graph.get(cur, []):
                if nei not in visit:
                    visit.add(nei)
                    paths[nei] = paths[cur] + [nei]
                    queue.append((nei, dist + 1))
                    
        return paths
    
if __name__ == '__main__':
    bfs = BFSPathfinder()
    
    path, distance = bfs.bfs('Viet Nam', 'France')
    
    if path:
        print(f"Path: {'->'.join(path)}")
        print(f"Distance: {distance}")
    else:
        print("No path found.")
