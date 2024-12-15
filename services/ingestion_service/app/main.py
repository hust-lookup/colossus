import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Request
import json
from publisher import publish_to_redis  

app = FastAPI()

@app.post("/receive-data")
async def receive_data(request: Request):
    try:
        body = await request.body()
        data = json.loads(body.decode("utf-8"))
        
        publish_to_redis(data)
        
        return {"status": "success", "message": "Dữ liệu đã được đẩy vào Redis"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
