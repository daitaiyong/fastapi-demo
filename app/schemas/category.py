from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_serializer


class CategoryCreateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=50, description="分类名称")

class CategoryUpdateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=50, description="分类名称")

class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="分类id")
    name: str = Field(description="分类名称")
    create_time: datetime = Field(description="创建时间")

    @field_serializer("create_time")
    def serialize_create_time(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")

class CategoryStatisticResponse(BaseModel):
    id: int = Field(description="分类id")
    name: str = Field(description="分类名称")
    product_count: int = Field(description="分类下的商品数量")