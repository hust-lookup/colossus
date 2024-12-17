import redis
import time
import json
from datetime import datetime
from validation import validate_data  # Import hàm validate_data từ validate.py
from utils import upload_to_s3_parquet  # Import hàm upload lên S3 từ s3_utils.py

# Kết nối tới Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def consume_from_redis():
    while True:
        all_data = []
        
        # Lấy toàn bộ dữ liệu từ hàng đợi Redis
        while True:
            data = redis_client.lpop('data_queue')  # Lấy dữ liệu từ queue
            if data:
                decoded_data = json.loads(data.decode('utf-8'))
                
                # Kiểm tra dữ liệu bằng hàm validate
                if validate_data(decoded_data):
                    all_data.append(decoded_data)  # Nếu hợp lệ thì thêm vào danh sách
                else:
                    print(f"Dữ liệu không hợp lệ, bỏ qua: {decoded_data}")
            else:
                break  # Không còn dữ liệu trong hàng đợi thì thoát vòng lặp

        if all_data:
            # Lưu dữ liệu lên AWS S3 dưới dạng Parquet
            upload_data_to_s3(all_data)

        # Chờ 30 giây trước khi lấy tiếp dữ liệu
        time.sleep(30)

def upload_data_to_s3(data):
    # Lấy thời gian hiện tại và tạo tên file theo ngày, giờ, phút
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
    s3_file_name = f"{current_time}.parquet"
    s3_bucket_name = 'hustinsight'  # Thay bằng tên bucket S3 của bạn

    # Upload dữ liệu lên S3 dưới dạng Parquet
    upload_to_s3_parquet(data, s3_bucket_name, s3_file_name)

if __name__ == "__main__":
    consume_from_redis()
