from fastapi import FastAPI
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlmodel import SQLModel
from datetime import datetime
from models.models import Turf, User
from schemas.schemas import TurfSchema, UserSchema
from src.turf import router as turf_router
from src.user import router as user_router
from src.area import transform_area_to_gdf

app = FastAPI()
app.include_router(turf_router)
app.include_router(user_router)
sql_engine = create_engine("postgresql+psycopg2://postgres:postgres@0.0.0.0:5432/killgen_db")
# We're not attaching a db yet, so this just lives in memory while the app runs.  Any restart empties it out

# Create the tables after starting the app, we probably don't want to do this every time
@app.on_event("startup")
def build_tables():
    SQLModel.metadata.create_all(sql_engine)

@app.get("/")
async def root():
    return {"message": "This is the base address of the API for managing the location data of the app"}
