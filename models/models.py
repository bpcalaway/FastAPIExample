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
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self):
        return f"{self.id}-{self.name}-{self.is_active}"

# Need to update this too
class Turf(Base):
    __tablename__ = "turf"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
