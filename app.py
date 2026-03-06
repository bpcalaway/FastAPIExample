from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlmodel import SQLModel
from datetime import datetime
from models.models import Turf, User
from schemas.schemas import TurfSchema, UserSchema
from src.turf import router as turf_router
from src.user import router as user_router
from src.area import transform_area_to_gdf
from src.sql import sql_engine

app = FastAPI()
app.include_router(turf_router)
app.include_router(user_router)
# We're not attaching a db yet, so this just lives in memory while the app runs.  Any restart empties it out

# Create the tables after starting the app, we probably don't want to do this every time
@app.on_event("startup")
def build_tables():
    SQLModel.metadata.create_all(sql_engine, tables=[Turf.__table__, User.__table__])
    print("Table Creation Complete")

@app.get("/")
async def root():
    return {"message": "This is the base address of the API for managing the location data of the app"}
