from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Text, Float, insert, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy_serializer import SerializerMixin
from src.sql import sql_engine

# 'Interesting' hack to utilize storing class models in a set
class Base(DeclarativeBase, SerializerMixin):
    __tablename__ = None

    def create(self):
        pass

    def get(self):
        pass

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    joined: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def create(username):
        with sql_engine.connect() as conn:
            user = conn.execute(insert(User).values(name=username))
            conn.commit()
        return user

    def get(id=None, name=None, is_active=True):
        conditions = [User.is_active == is_active]
        if id:
            conditions.append((User.id == id))
        if name:
            conditions.append((User.name == name))

        with sql_engine.connect() as conn:
            users = conn.execute(select(User).filter(*conditions))

        return [dict(r._mapping) for r in users]

    def __repr__(self):
        return f"{self.id}-{self.name}-{self.is_active}"

# Need to update this too
class Turf(Base):
    __tablename__ = "turf"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    upload_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    polygon: Mapped[str] = mapped_column(Text) #Will use to_wkt and from_wkt for shapely conversion

    # Store these separately for lookup purposes
    centroid_lat: Mapped[float] = mapped_column(Float)
    centroid_long: Mapped[float] = mapped_column(Float)
    area_sqkm: Mapped[float] = mapped_column(Float) # Not sure we need this, ignore for now
    area_avg_radius: Mapped[float] = mapped_column(Float)

    last_boosted: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    protected: Mapped[bool] = mapped_column(Boolean, default=False)


# In theory this should only need to be mapped once, on initial polygon capture, and one way to the captured
# polygon.  We may need to shift this in the future, but we'll do the naive approach for now
class ContestedTurfs(Base):
    __tablename__ = "contested_turfs"

    id: Mapped[int] = mapped_column(primary_key=True)
    captured_turf: Mapped[int] = mapped_column(ForeignKey(Turf.id))
    contesting_turf: Mapped[int] = mapped_column(ForeignKey(Turf.id)) #Cascade do work when this value is removed
    #Once the contest ends add this to their parent object and delete the record
    sub_polygon:  Mapped[str] = mapped_column(Text)

