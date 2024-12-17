# Sử dụng Python image
FROM python:3.11-slim

# Cài đặt các thư viện cần thiết
WORKDIR /app

# Copy file requirements.txt (nếu có) và cài đặt các gói
RUN pip install python-multipart
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Copy toàn bộ mã nguồn của ứng dụng vào container
COPY . /app

# Chạy FastAPI với uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
