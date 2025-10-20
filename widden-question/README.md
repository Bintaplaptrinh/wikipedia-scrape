# 🌐 Six Degrees of Wikipedia - Extended Project

## Mở rộng đề tài

Dự án này mở rộng từ bài tập **Wikipedia Population Data** để phân tích **Information Influence** và **Connectivity** của các quốc gia thông qua Wikipedia link graph.

---

## 🎯 Research Questions

### **Q4: Quốc gia nào có "tầm ảnh hưởng thông tin" lớn nhất?**

**Metrics sử dụng:**
- **Degree Centrality:** Số lượng connections
- **PageRank:** Importance dựa trên incoming links
- **Betweenness Centrality:** Tần suất xuất hiện trên shortest paths

**Hypothesis:** Large, developed countries (US, UK, China) sẽ có influence cao nhất.

---

### **Q5: Có mối tương quan nào giữa dân số/kinh tế và "mức độ kết nối"?**

**Analysis:**
- **Population vs Connectivity:** Pearson correlation
- **Density vs Connectivity:** Spearman correlation
- **Regional Patterns:** Group by Region

**Hypothesis:** 
- High population → High connectivity (moderate correlation)
- Density không tương quan mạnh với connectivity

---

## Architecture

```
widden-question/
├── load_data.py          # Load countries từ MongoDB
├── main.py               # Main orchestrator
│
├── scrape/
│   └── scrape_wiki.py    # Wikipedia API scraper (multi-threaded)
│
├── bfs/
│   └── bfs_pathfinder.py # ⭐ BFS pathfinding (CORE)
│
├── analytic/
│   ├── q4.py            # Influence analysis (NetworkX)
│   └── q5.py            # Correlation analysis (Scipy)
│
└── visualize/
    └── visualize.py     # Plotly visualization
```

---

## Quick Start

```bash
# 1. Load countries
python load_data.py

# 2. Scrape graph
cd scrape && python scrape_wiki.py

# 3. Test BFS
cd ../bfs && python bfs_pathfinder.py

# 4. Analyze
cd ../analytic
python q4.py  # Q4: Influence
python q5.py  # Q5: Correlation

# 5. Run full pipeline
cd .. && python main.py
```

Xem chi tiết: **[QUICKSTART.md](QUICKSTART.md)**

---

## Results Preview

### **Q4: Top Influential Countries**
```
1. United States - 0.856
2. United Kingdom - 0.746
3. China - 0.723
4. France - 0.689
5. Germany - 0.654
```

### **Q5: Correlations**
```
Population vs Connectivity: r = 0.42 (p < 0.001)
→ en: Moderate positive correlation; vi: sự tương quan giữa dấn số và mức độ kết nối

Density vs Connectivity: ρ = 0.18 (p = 0.08)
→ Weak correlation (not significant), sự tương quan giữa mật độ dân số và mức độ kết nối
```

---

## Key Features

**BFS Implementation** - Shortest path finding (CORE requirement)  
**Multi-threaded Scraping** - Fast Wikipedia data collection  
**NetworkX Analysis** - Degree, PageRank, Betweenness  
**Statistical Analysis** - Pearson & Spearman correlation  
**Interactive Visualization** - Plotly charts  

---

## Dependencies

```bash
pip install wikipediaapi networkx scipy plotly pymongo python-dotenv
```

---

## Documentation

- **[CODE_REVIEW.md](CODE_REVIEW.md)** - Bug fixes & code quality

---

## Academic Context

**Course:** Quản Lí Dữ Liệu Lớn  
**Topic:** Wikipedia Graph Analysis + BFS Algorithm  
**Dataset:** 232 countries + ~3000-5000 Wikipedia links  
**Techniques:** BFS, Graph Theory, Network Analysis, Statistical Correlation  

---

## Notes

- BFS là **requirement bắt buộc** và đã được implement đầy đủ
- Project **KHÔNG dùng Hadoop** (simplified version)
- Dùng NetworkX thay vì implement algorithms từ đầu
- Data source: MongoDB từ project gốc (wikipedia-scrape)