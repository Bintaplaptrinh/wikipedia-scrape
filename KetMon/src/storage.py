from pymongo import MongoClient
import pandas as pd
import os
from dotenv import load_dotenv
from scrape import join_table, scrape_area_data, scrape_poplulation_data


load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")


def save_to_mongodb(df):
    try:
        client= MongoClient(MONGODB_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        collection.insert_many(df.to_dict(orient="records"))
        print("data saved to mongodb")
        
    except Exception as e:
        print(f"error in connection step: {e}")
        return
    
    
def load_from_mongodb():
    try:
        client = MongoClient(MONGODB_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        data = list(collection.find())
        df = pd.DataFrame(data)
        print("data loaded from mongodb")
        return df
    except Exception as e:
        print(f"error loading from mongodb: {e}")
        return


def save_to_csv(df, filename, location="../data/"):
    try:
        #save df to csv in other location
        df.to_csv(location + filename, index=False)
        print(f"data saved to {location + filename}")
    except Exception as e:
        print(f"error saving to csv: {e}")
        return

#test scrape and convert to csv
df1, table_raw_html = scrape_poplulation_data()
df2, raw = scrape_area_data()
df = join_table(df1, df2)
save_to_csv(df, "wiki_pop_raw.csv")
print(table_raw_html)
print(raw)