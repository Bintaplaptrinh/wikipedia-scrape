import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://en.wikipedia.org/wiki/United_Nations_geoscheme"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/123.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# 🎯 Chỉ lấy phần nội dung chính (bỏ phần mục lục)
content = soup.find("div", {"class": "mw-parser-output"})

data = []
region = None
subregion = None

for tag in content.find_all(["h2", "h3", "ul"]):
    if tag.name == "h2":
        region = tag.get_text(strip=True).replace("[edit]", "")
        subregion = None
    elif tag.name == "h3":
        subregion = tag.get_text(strip=True).replace("[edit]", "")
    elif tag.name == "ul":
        for li in tag.find_all("li", recursive=False):
            a = li.find("a")
            if not a:
                continue
            country = a.get_text(strip=True)

            # Bỏ các dòng không phải tên quốc gia
            if any(x in country.lower() for x in ["edit", "geoscheme", "references", "see also"]):
                continue
            if region and subregion and country:
                data.append({
                    "Country": country,
                    "Region": region,
                    "Subregion": subregion
                })

df = pd.DataFrame(data)

print(f"✅ Crawled {len(df)} countries/regions")
print(df.head(10))
print(df.tail(10))

#df.to_csv("united_nations_geoscheme.csv", index=False, encoding="utf-8-sig")
#print("\n💾 Saved file: united_nations_geoscheme.csv")
