from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_serializer
from sqlalchemy import desc


class ProductCreateRequest(BaseModel):
    category_id: int = Field(gt=0, description="所属分类id")
    name: str = Field(min_length=1, max_length=50, description="商品名称")
    price: Decimal = Field(
        gt=0, decimal_places=2, max_digits=8, description="商品单价(元)"
    )
    stock: int = Field(default=0, ge=0, description="库存数量")
    self_status: bool = Field(default=True, description="是否上架")

class ProductUpdateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    category_id: int | None = Field(default=None, gt=0, description="所属分类id")
    name: str | None = Field(default=None, min_length=1, max_length=50, description="商品名称")
    price: Decimal | None = Field(
        default=None, gt=0, decimal_places=2, max_digits=8, description="商品单价(元)"
    )
    stock: int | None= Field(default=None, ge=0, description="库存数量")
    self_status: bool | None= Field(default=None, description="是否上架")

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="商品id")
    category_id: int = Field(description="所属分类id")
    name: str = Field(description="商品名称")
    price: Decimal = Field(description="商品单价(元)")
    stock: int = Field(description="库存数量")
    self_status: bool = Field(description="是否上架")
    create_time: datetime = Field(description="创建时间")

    @field_serializer("price")
    def serialize_price(self, value: Decimal) -> str:
        return f"{value: 2f}"
    
    @field_serializer("create_time")
    def serialize_create_time(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")

class ProductCategoryNameResponse(ProductResponse):
    category_name: str = Field(description="分类名称")


class ProductCountResponse(BaseModel):
    total: int = Field(description="全部商品数量")

class ProductPageResponse(BaseModel):
    items: list[ProductCategoryNameResponse] = Field(description="当前页商品")
    total: int = Field(description="符合条件的商品数量")
    page: int = Field(description="当前页码")
    page_size: int = Field(description="每页条数")

