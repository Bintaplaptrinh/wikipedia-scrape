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

## Chạy dự án

```
docker-compose up -d
docker-compose exec app python src/main.py
```

## Kiểm tra kết quả 

Xem dữ liệu trên HDFS:
```
docker-compose exec app hdfs dfs -cat /data/wiki/silver/pop_clean.jsonl

```
## Down docker
```
docker-compose down -v
```