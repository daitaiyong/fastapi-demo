from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa
from decimal import Decimal
from sqlalchemy import Boolean, ForeignKey, Numeric
from app.database import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.category import Category

class Product(Base):
    __tablename__ = "product"
    __table_args__ = {"comment":"商品表"}    

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False, comment="所属分类id")
    name: Mapped[str] = mapped_column(sa.String(50), nullable=True, comment="商品名称")
    price: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False, comment="商品单价(元)")
    stock: Mapped[int] = mapped_column(nullable=False, default=0, comment="商品库存数量")
    self_status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, comment="商品是否上架") 
    category: Mapped["Category"] = relationship(back_populates="product")  