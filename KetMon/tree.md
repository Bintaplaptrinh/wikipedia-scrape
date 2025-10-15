project_root/
├── .env                  # (Tùy chọn) File chứa các biến môi trường nhạy cảm (ví dụ: API keys)
├── requirements.txt      # Danh sách các thư viện Python cần cài đặt
├── docker-compose.yml    # (Nếu dùng Docker) Định nghĩa các dịch vụ Docker (Spark Master, Worker, MongoDB)
├── README.md             # Mô tả dự án, cách cài đặt, cách chạy, kết quả phân tích
│
├── src/                  # Chứa tất cả mã nguồn Python chính
│   ├── __init__.py       # Để biến 'src' thành một Python package
│   ├── scraper.py        # Mã nguồn cào dữ liệu từ Wiki (dân số, diện tích, khu vực)
│   ├── spark_etl_q123.py # Mã nguồn PySpark: ETL, tính density, pop_bucket, Q1, Q2, Q3
│   ├── graph_crawler.py  # Mã nguồn Python: Dùng Wiki API để cào dữ liệu đồ thị, BFS, multi-threading
│   └── spark_graph_analysis_q456.py # Mã nguồn PySpark: Đọc dữ liệu đồ thị, phân tích Q4, Q5, Q6
│
├── data/                 # Chứa tất cả dữ liệu thô và đã xử lý
│   ├── raw/              # Dữ liệu thô ban đầu sau khi cào
│   │   └── countries_raw.csv    # Dữ liệu dân số, diện tích, khu vực thô (từ scraper.py)
│   │
│   ├── processed/        # Dữ liệu đã được làm sạch và chuẩn hóa
│   │   ├── pop_clean.parquet    # Dữ liệu dân số đã ETL (từ spark_etl_q123.py)
│   │   └── country_graph.jsonl  # Dữ liệu đồ thị (từ graph_crawler.py)
│   │
│   └── outputs/          # Kết quả cuối cùng của các phân tích
│       ├── q1_region_population.csv
│       ├── q2_top_density.csv
│       ├── q3_pop_bucket_distribution.csv
│       ├── q4_top_influence.csv
│       ├── q5_correlation_result.txt
│       └── # Thêm các file kết quả khác (biểu đồ, bảng...)
│
├── notebooks/            # (Tùy chọn) Jupyter Notebooks để khám phá dữ liệu hoặc trình bày kết quả
│   ├── data_exploration.ipynb
│   └── final_presentation.ipynb
│
└── .gitignore            # Các file/thư mục cần bỏ qua khi commit lên Git (ví dụ: .env, data/, __pycache__, venv/)