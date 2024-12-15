# Bắt đầu từ image Python chính thức
FROM python:3.9-slim

# Cài đặt các phụ thuộc cần thiết và Redis
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    redis-server \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép tất cả mã nguồn vào trong container
COPY . /app

# Cài đặt các yêu cầu phụ thuộc từ file requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Mở cổng mà FastAPI sẽ chạy (ví dụ: 8000)
EXPOSE 8000
EXPOSE 6379 


# Lệnh để khởi động Redis và FastAPI cùng lúc
CMD ["sh", "-c", "service redis-server start & python3 consumer.py & uvicorn main:app --host 0.0.0.0 --port 8000"]
