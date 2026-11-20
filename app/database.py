
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from app.config import settings
from sqlalchemy import DateTime, INTEGER, Integer, create_engine, engine


engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, sort_order= -1, comment="主键id")
    create_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, comment="创建时间")