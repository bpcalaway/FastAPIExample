from datetime import datetime
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# 'Interesting' hack to utilize storing class models in a set
class Base(DeclarativeBase):
    __tablename__ = None

    def create(self):
        pass

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    # join: datetime Too much work lol
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

# Need to update this too
class Turf(Base):
    __tablename__ = "turf"
    # Defined set of GPSPoint objects, use this to define the area specifically
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    #vertices: set[GPSPoint]
    #claimedSong: SongChoice