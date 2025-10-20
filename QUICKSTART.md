# QUICK START

## Chạy nhanh 3 bước:

### Scrape → MongoDB (3 collections)
```bash
cd src
python main.py
```

### ETL → HDFS (Test local trước)
```bash
# Export MongoDB
mongoexport --collection=wiki_joined --out=../tmp/wiki_joined.jsonl

# Test local
cd ..
cat tmp/wiki_joined.jsonl | python hadoop/etl/mapper.py | sort | python hadoop/etl/reducer.py > tmp/pop_clean.jsonl

# Chạy trên Hadoop
hadoop jar $HADOOP_STREAMING_JAR \
  -input /data/wiki/bronze/wiki_joined.jsonl \
  -output /data/wiki/silver/pop_clean_temp \
  -mapper hadoop/etl/mapper.py \
  -reducer hadoop/etl/reducer.py \
  -file hadoop/etl/mapper.py \
  -file hadoop/etl/reducer.py
```

### Analytics (Q1, Q2, Q3)
```bash
# Q1: Tổng dân số/region
cat tmp/pop_clean.jsonl | python hadoop/q1/mapper.py | sort | python hadoop/q1/reducer.py

# Q2: Top 10 mật độ
cat tmp/pop_clean.jsonl | python hadoop/q2/mapper.py | sort | python hadoop/q2/reducer.py

# Q3: Phân phối pop_bucket
cat tmp/pop_clean.jsonl | python hadoop/q3/mapper.py | sort | python hadoop/q3/reducer.py
```

---

## Chi tiết xem:
- `README.md` - Hướng dẫn đầy đủ

## Requirements:
```bash
pip install pandas beautifulsoup4 requests pymongo python-dotenv
```
