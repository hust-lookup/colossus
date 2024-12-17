import boto3
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from io import BytesIO

# Cấu hình kết nối với AWS S3
s3_client = boto3.client(
    's3',
    aws_access_key_id='',  # Thay bằng API Key
    aws_secret_access_key='',  # Thay bằng API Secret
    region_name='ap-southeast-1' 
)

def upload_to_s3_parquet(data, bucket_name, file_name):
    """
    Upload dữ liệu dạng Parquet lên S3
    """
    # Chuyển dữ liệu từ dict hoặc list of dict thành pandas DataFrame
    df = pd.DataFrame(data)

    # Chuyển DataFrame thành bảng Arrow
    table = pa.Table.from_pandas(df)

    # Tạo một stream nhớ tạm để lưu dữ liệu Parquet
    buffer = BytesIO()
    pq.write_table(table, buffer)
    
    # Đặt con trỏ về đầu stream
    buffer.seek(0)
    
    # Upload dữ liệu Parquet lên S3
    s3_client.upload_fileobj(buffer, bucket_name, file_name)
    print(f"Đã upload dữ liệu lên S3: {file_name}")
