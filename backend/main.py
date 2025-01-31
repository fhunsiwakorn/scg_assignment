from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers.sensor import routes_sensor as rs_rq_router
import uvicorn

# สร้าง FastAPI app
app = FastAPI()

# สร้างตารางในฐานข้อมูล
models.Base.metadata.create_all(bind=engine)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# รวม router สำหรับ sensor
app.include_router(rs_rq_router, prefix="/sensor", tags=["Sensor"])

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
