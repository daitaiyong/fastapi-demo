from itertools import product

import sqlalchemy as sa
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.product import Product

class Category(Base):
    __tablename__ = "categories"
    __table_args__ = {"comment":"商品分类表"}
    name: Mapped[str] = mapped_column(
        sa.String(50), nullable=True, comment="分类名称"
        )
    product: Mapped[list["Product"]] = relationship(back_populates="category") 
