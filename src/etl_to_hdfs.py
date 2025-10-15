import pandas as pd
import os
from storage import load_from_mongodb
import subprocess
import time
import json

def wait_hdfs():
    print("waiting for hdfs")
    for i in range(30):
        try:
            result = subprocess.run(
                ["hdfs", "dfs", "-ls", "/"],
                capture_output=True,
                timeout=10,
            )
            if result.returncode == 0:
                print("hdfs is ready")
                return True
        except subprocess.TimeoutExpired:
            print("hdfs not ready yet, retrying")
            time.sleep(5)

    return False

def etl_data(df):
    if df is None:
        print("data is none")
        return
    
    try:
        print("starting etl data")
        
        df_clean = df.copy()
        
        if pd.isna(df_clean).all().all():
            print("data is all NaN")
            return None
        
        try:
            df_clean['population'] = pd.to_numeric(df_clean['population'], errors='coerce')
            df_clean['area_km2'] = pd.to_numeric(df_clean['area_km2'], errors='coerce')
            df_clean['density'] = pd.to_numeric(df_clean['density'], errors='coerce')

        except Exception as e:
            print(f"error in etl step: {e}")
            return
        df_clean = df_clean.dropna(subset=['population', 'area_km2', 'density'])
        df_clean = df_clean[df_clean['population'] > 0]
        df_clean = df_clean[df_clean['area_km2'] > 0]
        df_clean = df_clean[df_clean['density'] > 0]
        df_clean = df_clean.drop(columns=['_id', 'std_location', 'std_Country'], errors='ignore')
        df_clean = df_clean.reset_index(drop=True)
        
        #standardize country sub and region names
        df_clean['Region'] = df_clean['Region'].str.title().str.strip()
        df_clean['Subregion'] = df_clean['Subregion'].str.title().str.strip
        
        #add pop_bucket
        print("adding pop_bucket")
        df_clean['pop_bucket'] = pd.cut(
            df_clean['population'],
            bins=[0, 1000000, 10000000, 50000000, 100000000, float('inf')],
            labels=['<1M', '1M-10M', '10M-50M', '50M-100M', '>100M']
        )
        
        df_clean['pop_bucket'] = df_clean['pop_bucket'].astype(str)
        print(df_clean['pop_bucket'].value_counts())
        
        #fliter empyty country
        before = len(df_clean)
        df_clean = df_clean[df_clean['Country'].notna() & (df_clean['Country'].str.strip() != '')]
        
        after = len(df_clean)
        print(f"filtered empty country: {before} -> {after}")
        
        final_df = df_clean[[
            'Country', 'Region', 'Subregion', 'population', 'area_km2', 'density', 'pop_bucket'
        ]]
        
        print("data etl completed")
        return df_clean
    except Exception as e:
        print(f"error in etl step: {e}")
        return
    
def save_to_jsonl(df, filename, location="/data/wiki/silver/pop_clean.jsonl"):
    if df is None:
        print("data is none")
        return
    try:
        print(f"saving to {location}")
        
        local_temp = "tmp/pop_clean.jsonl"
        print(f"saving to local temp {local_temp}")
        
        with open(local_temp, 'w', encoding='utf-8') as f:
            for _, row in df.iterrows():
                json_record = row.to_json(force_ascii=False)
                f.write(json_record + '\n')
                
        print(f"saved {len(df)} records to local temp {local_temp}")
        
        print(f"uploading to hdfs {location}")
        hdfs_dir = os.path.dirname(location)
        
        result = subprocess.run(
            ["hdfs", "dfs", "-mkdir", "-p", hdfs_dir],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0 and 'File exists' not in result.stderr:
            print(f"error creating hdfs directory {hdfs_dir}: {result.stderr}")
            return
        else:
            print(f"hdfs directory {hdfs_dir} is ready")
            
        result = subprocess.run(
            ["hdfs", "dfs", "-put", "-f", local_temp, location],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"error uploading to hdfs: {result.stderr}")
            return
        else:
            print(f"uploaded to hdfs {location} successfully")
            
        #check file
        result = subprocess.run(
            ["hdfs", "dfs", "-ls", location],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"error checking hdfs file: {result.stderr}")
            return
        else:
            print(f"hdfs file {location} exists:")
            print(result.stdout)
        
        os.remove(local_temp)
        return True
    
    except Exception as e:
        print(f"error saving to hdfs jsonl: {e}")
        import traceback
        traceback.print_exc()
        return False