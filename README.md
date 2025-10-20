# Bài tập lớn: Wikipedia – Bảng dân số quốc gia (UN)
Nội dung bài tập:
- Parse bảng HTML lớn → tổng hợp theo khu vực.
- Scrape → Mongo (wiki_pop_raw): lưu nguyên table_html + record parsed:
{ country, region, subregion, population:int, area_km2:float, density:float }
- ETL: bỏ dấu phẩy, N/A → null; chuẩn region/subregion; thêm pop_bucket.
- HDFS: /data/wiki/silver/pop_clean.jsonl
- MR:
•	Q1 (tổng dân số/region): region\tpopulation → cộng.
•	Q2 (top mật độ): có thể 1-pass bằng reducer giữ top-10 theo density (lọc area_km2>0).
•	Q3 (phân phối pop_bucket): pop_bucket\t1.
- Pitfall: một vài hàng tiêu đề/ghi chú len vào parse → cần lọc country rỗng..


# HƯỚNG DẪN CHẠY DỰ ÁN - Wikipedia Population Scraping & MapReduce

## Cấu trúc dự án

```
wikipedia-scrape/
├── src/                      # Source code chính
│   ├── main.py              # Orchestrator (Phase 1: Scrape)
│   ├── scrape.py            # Logic scraping
│   ├── storage.py           # MongoDB operations
│   └── standardize_country.py
│
├── hadoop/                   # MapReduce jobs
│   ├── etl/                 # ETL: Clean data
│   │   ├── mapper.py
│   │   └── reducer.py
│   ├── q1/                  # Q1: Tổng dân số/region
│   │   ├── mapper.py
│   │   └── reducer.py
│   ├── q2/                  # Q2: Top 10 mật độ
│   │   ├── mapper.py
│   │   └── reducer.py
│   └── q3/                  # Q3: Phân phối pop_bucket
│       ├── mapper.py
│       └── reducer.py
│
├── data/                     # Local data
├── tmp/                      # Temporary files
└── requirements.txt
```

---

## HƯỚNG DẪN CHẠY

### **SCRAPE & SAVE TO MONGODB**

```bash
# Chạy scraping
cd src
python main.py
```

**Kết quả:**
- 3 collections trong MongoDB:
  - `wiki_pop_raw` - Dữ liệu population gốc + HTML table
  - `wiki_area_raw` - Dữ liệu area/region gốc + raw text
  - `wiki_joined` - Bảng đã join + HTML table


### **PHASE 2: ETL TO HDFS (MapReduce)**

#### Bước 1: Export từ MongoDB
```bash
mongoexport --uri="mongodb://localhost:27017" \
  --db=your_db_name \
  --collection=wiki_joined \
  --out=tmp/wiki_joined.jsonl
```

#### Bước 2: Upload lên HDFS
```bash
hdfs dfs -mkdir -p /data/wiki/bronze
hdfs dfs -put -f tmp/wiki_joined.jsonl /data/wiki/bronze/
```

#### Bước 3: Chạy MapReduce ETL
```bash
hadoop jar $HADOOP_STREAMING_JAR \
  -input /data/wiki/bronze/wiki_joined.jsonl \
  -output /data/wiki/silver/pop_clean_temp \
  -mapper hadoop/etl/mapper.py \
  -reducer hadoop/etl/reducer.py \
  -file hadoop/etl/mapper.py \
  -file hadoop/etl/reducer.py
```

#### Bước 4: Merge kết quả
```bash
hdfs dfs -getmerge /data/wiki/silver/pop_clean_temp/part-* tmp/pop_clean.jsonl
hdfs dfs -put -f tmp/pop_clean.jsonl /data/wiki/silver/pop_clean.jsonl
```

**Kết quả:**
- File `/data/wiki/silver/pop_clean.jsonl` trên HDFS
- Dữ liệu đã clean: bỏ dấu phẩy, N/A→null, thêm pop_bucket


### **ANALYTICS (MapReduce)**

#### Q1: Tổng dân số theo Region
```bash
hadoop jar $HADOOP_STREAMING_JAR \
  -input /data/wiki/silver/pop_clean.jsonl \
  -output /data/wiki/results/q1_population_by_region \
  -mapper hadoop/q1/mapper.py \
  -reducer hadoop/q1/reducer.py \
  -file hadoop/q1/mapper.py \
  -file hadoop/q1/reducer.py

# Xem kết quả
hdfs dfs -cat /data/wiki/results/q1_population_by_region/part-* | sort -t$'\t' -k2 -nr
```

#### Q2: Top 10 mật độ cao nhất
```bash
hadoop jar $HADOOP_STREAMING_JAR \
  -input /data/wiki/silver/pop_clean.jsonl \
  -output /data/wiki/results/q2_top_density \
  -mapper hadoop/q2/mapper.py \
  -reducer hadoop/q2/reducer.py \
  -file hadoop/q2/mapper.py \
  -file hadoop/q2/reducer.py

# Xem kết quả
hdfs dfs -cat /data/wiki/results/q2_top_density/part-*
```

#### Q3: Phân phối Population Bucket
```bash
hadoop jar $HADOOP_STREAMING_JAR \
  -input /data/wiki/silver/pop_clean.jsonl \
  -output /data/wiki/results/q3_pop_bucket \
  -mapper hadoop/q3/mapper.py \
  -reducer hadoop/q3/reducer.py \
  -file hadoop/q3/mapper.py \
  -file hadoop/q3/reducer.py

# Xem kết quả
hdfs dfs -cat /data/wiki/results/q3_pop_bucket/part-*
```


## TEST LOCAL (KHÔNG CẦN HADOOP)

### Test ETL Mapper/Reducer
```bash
cat tmp/wiki_joined.jsonl | python hadoop/etl/mapper.py | sort | python hadoop/etl/reducer.py > tmp/test_etl.jsonl
```

### Test Q1
```bash
cat tmp/pop_clean.jsonl | python hadoop/q1/mapper.py | sort | python hadoop/q1/reducer.py
```

### Test Q2
```bash
cat tmp/pop_clean.jsonl | python hadoop/q2/mapper.py | sort | python hadoop/q2/reducer.py
```

### Test Q3
```bash
cat tmp/pop_clean.jsonl | python hadoop/q3/mapper.py | sort | python hadoop/q3/reducer.py
```


## MÔ TẢ LOGIC

### ETL Mapper
- Bỏ dấu phẩy trong số
- Chuyển N/A → null
- Filter: country rỗng, population/area/density ≤ 0
- Chuẩn hóa Region/Subregion (title case)
- Thêm pop_bucket: <1M, 1M-10M, 10M-50M, 50M-100M, >100M

### Q1: Tổng dân số/Region
- Mapper: region → population
- Reducer: Sum(population) group by region

### Q2: Top 10 mật độ
- Mapper: density → json_record (filter area_km2 > 0)
- Reducer: Heap giữ top 10, sort DESC

### Q3: Phân phối pop_bucket
- Mapper: pop_bucket → 1
- Reducer: Count group by pop_bucket

---

## YÊU CẦU

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
pandas
beautifulsoup4
requests
pymongo
python-dotenv
```

**Environment (.env):**
```
MONGODB_URI=mongodb://localhost:27017
DB_NAME=wikipedia_db
```


## LLƯU Ý

1. **Mapper/Reducer phải có quyền execute:**
   ```bash
   chmod +x hadoop/**/*.py
   ```

2. **HDFS phải sẵn sàng:**
   ```bash
   hdfs dfs -ls /
   ```

3. **MongoDB phải chạy:**
   ```bash
   mongod --port 27017
   ```

4. **Test local trước khi chạy Hadoop!**


## KẾT QUẢ MONG ĐỢI

| Phase | Output | Location |
|-------|--------|----------|
| Phase 1 | 3 MongoDB collections | `wiki_pop_raw`, `wiki_area_raw`, `wiki_joined` |
| Phase 2 | Clean JSONL | `/data/wiki/silver/pop_clean.jsonl` |
| Q1 | Region populations | `/data/wiki/results/q1_*/` |
| Q2 | Top 10 densities | `/data/wiki/results/q2_*/` |
| Q3 | Bucket distribution | `/data/wiki/results/q3_*/` |

