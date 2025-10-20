from pymongo import MongoClient
from dotenv import load_dotenv
import json
import os

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")

def load_countries():
    try:
        client = MongoClient(MONGODB_URI)
        db = client[DB_NAME]
        collection = db['wiki_pop_raw'] #construction document: Country,Region','Subregion','population','area_km2','density'
        
        countries = []
        for cou in collection.find({}, {'_id': 0}):
            countries.append(cou)
            
        with open('countries.jsonl', 'w', encoding='utf-8') as f:
            json.dump(countries, f, ensure_ascii=False, indent=2)
        print(f"loaded {len(countries)} countries from wiki_pop_raw")
        client.close()
        return countries
    except Exception as e:
        print(f"error loading countries: {e}")
        return []
    
if __name__ == '__main__':
    load_countries()