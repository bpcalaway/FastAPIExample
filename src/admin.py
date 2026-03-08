from fastapi import APIRouter
from src.sql import sql_engine
from sqlmodel import SQLModel
from models.models import Turf, User
from schemas.schemas import TurfSchema, UserSchema

router = APIRouter(prefix="/Admin", tags=["Admin"])

@router.post("/Admin/CreateAll")
def create_all_tables():
    """
    Creates all of the tables according to our model file definitions, will fail without a DropAll call or a fresh DB
    """
    SQLModel.metadata.create_all(sql_engine, tables=[Turf.__table__, User.__table__])
    return {"message": "Table Creation Complete"}

@router.post("/Admin/LoadAll")
def load_all_tables():
    """
    TODO Define some dev data, that we can use for testing.
    """
    return {"message": "Not yet implemented"}

@router.post("/Admin/DropAll")
def drop_all_tables():
    """
    Lazy and nasty function to delete all data, when you're messing with format you need to do both.
    """
    SQLModel.metadata.drop_all(sql_engine, tables=[Turf.__table__, User.__table__])
    return {"message": "Dropped All Tables, please recreate"}