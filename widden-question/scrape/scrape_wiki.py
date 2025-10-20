import wikipediaapi
import json
import sys
import time
from collections import defaultdict
import threading

class CountryScrape:
    def __init__(self):
        self.wiki = wikipediaapi.Wikipedia(
            language='en',
            user_agent='CountryScrape/1.0 (student.project@example.com)'
        )
        self.country_set = set() #to l9oad from countries.json
        self.graph = defaultdict(list)
        self.lock = threading.Lock()
        
    def load_countries(self, filepath ='./countries.jsonl'):
        with open(filepath, 'r', encoding='utf-8') as f:
            countries = json.load(f)
            for cou in countries:
                name = cou.get('Country')
                if name:
                    self.country_set.add(name)
                    
    def scrape_coun_links(self, country_name):
        page = self.wiki.page(country_name)
        if not page.exists():
            return []
        
        links = page.links
        linked_countries = []
        for title in links:
            if title in self.country_set and title != country_name:
                linked_countries.append(title)
        return linked_countries
    
    def build_graph(self):
        
        
        con_list = list(self.country_set)
        total_con = len(con_list)
        print(f"total countries to scrape: {total_con}")
        
        chunks = total_con // 5
        threads = []
        for i in range(5):
            start_idx = i * chunks
            end_idx = (i + 1) * chunks if i < 4 else total_con
            t = threading.Thread(target=self._scrape_thread, args=(start_idx, end_idx))
            threads.append(t)
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def _scrape_thread(self, start_idx, end_idx):
        country_list = list(self.country_set)
        
        for i in range(start_idx, end_idx):
            country = country_list[i]
            print(f"[Thread {threading.current_thread().name}] Scraping {country}...")

            linked_countries = self.scrape_coun_links(country)
                                                  
            with self.lock:
                self.graph[country] = linked_countries
            
            time.sleep(0.1)
        # for country in self.country_set:
        #     print(f"scraping links for {country}...")
        #     linked_countries = self.scrape_coun_links(country)
        #     self.graph[country] = linked_countries
        #     time.sleep(1)

    def save_graph(self, filepath='../graph.json'):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.graph, f, ensure_ascii=False, indent=4)
            
if __name__ == '__main__':
    scraper = CountryScrape()
    print("loading countries...")
    scraper.load_countries()
    print(f"loaded {len(scraper.country_set)} countries.")
    
    print("building graph...")
    scraper.build_graph()
    
    print("saving graph...")
    scraper.save_graph()
    print("graph saved to widden-question/graph.json")
