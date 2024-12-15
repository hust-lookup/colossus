import redis
import json

# Kết nối tới Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def publish_to_redis(data):
    try:
        # Chuyển đổi dữ liệu thành chuỗi JSON
        data_json = json.dumps(data)
        
        # Đẩy dữ liệu vào Redis list với tên 'data_queue'
        redis_client.rpush('data_queue', data_json)
        print(f"Đã đẩy dữ liệu vào Redis: {data_json}")
    except Exception as e:
        print(f"Lỗi khi đẩy dữ liệu vào Redis: {e}")
