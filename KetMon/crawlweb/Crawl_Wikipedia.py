import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


url = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population_density"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

try:
    response = session.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    table_classes = ['wikitable sortable', 'wikitable', 'sortable wikitable', 'wikitable sortable mw-datatable']
    table = None
    for cls in table_classes:
        table = soup.find('table', {'class': cls})
        if table:
            break

    if not table:
        raise Exception("Table not found!")

    rows = table.find_all('tr')
    data = []

    for row in rows[1:]:  
        cols = row.find_all('td')
        if len(cols) >= 4:
            location = cols[0].text.strip()
            density_km_str = cols[1].text.strip().replace(',', '').replace('−', '-') if len(cols) > 1 else ''
            population_str = cols[3].text.strip().replace(',', '') if len(cols) > 3 else ''
            area_km_str = cols[4].text.strip().replace(',', '') if len(cols) > 4 else ''
            if location:
                data.append({
                    'location': location,
                    'density': density_km_str,
                    'population': population_str,
                    'area_km2': area_km_str
                })

    df = pd.DataFrame(data)

    df['density'] = pd.to_numeric(df['density'], errors='coerce')
    df['population'] = pd.to_numeric(df['population'], errors='coerce').astype('Int64')
    df['area_km2'] = pd.to_numeric(df['area_km2'], errors='coerce').astype(float)

    df = df.replace('', pd.NA)
    df = df[df['location'].notna() & (df['location'] != '')]

    print("\nFirst 10 rows:")
    print(df.head(10))
    print("\nLast 10 rows:")
    print(df.tail(10))

    df.to_csv('pop_density_clean.csv', index=False)

except requests.RequestException as e:
    print(f"Error fetching page: {e}")
except Exception as e:
    print(f"Error processing data: {e}")

finally:
    session.close()