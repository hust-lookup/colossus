from typing import Union

from fastapi import FastAPI

app = FastAPI()

# TODO: 
# 1. Data Processing -> Version (DVC) -> S3 (Auto) Airflow + Spark(pyspark) 
# 2. S3 -> Model Training -> Version (DVC) -> S3 (Auto) Airflow + Spark(pyspark) 

# Admin 

# APIs 
# /recommend/{customer_id} -> GET -> (S3) -> load torch model -> Danh sach san pham ma khach hang do co the mua


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/recommend/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"id": item_id, "q": q}
