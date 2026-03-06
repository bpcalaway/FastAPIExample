from sqlalchemy import create_engine, select

sql_engine = create_engine("postgresql+psycopg2://postgres:postgres@0.0.0.0:5432/killgen_db")