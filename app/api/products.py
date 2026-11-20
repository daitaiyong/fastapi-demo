from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Path

from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.common.response import Response
from app.schemas.product import ProductCountResponse, ProductCreateRequest,ProductUpdateRequest, ProductPageResponse, ProductResponse
from app.services import product_service 

router = APIRouter(prefix="/products", tags=["商品相关接口"])

@router.post("", response_model=Response, summary="创建商品")
def create_product(
    payload: ProductCreateRequest, 
    db: Annotated[Session, Depends(get_db)],
    ):
    return Response.success(
        data=ProductResponse.model_validate(product_service.create_product(db, payload))
    )

@router.patch("/{product_id}", response_model=Response, summary="更新商品信息")
def update_product(
    payload: ProductUpdateRequest, 
    product_id: int,
    db: Annotated[Session, Depends(get_db)],
    ):
    update_product = product_service.update_product(db, payload, product_id)
    return Response.success(
        data=ProductResponse.model_validate(update_product)
    )

@router.delete("/{product_id}", response_model=Response, summary="删除商品")
def delete_product(
    product_id: int,
    db: Annotated[Session, Depends(get_db)],
    ):
    delete_product = product_service.delete_product(db, product_id)
    return Response.success(delete_product)

@router.get("", response_model=Response, summary="分页查询商品")
def get_page_products(
    db: Annotated[Session, Depends(get_db)],
    keyword: Annotated[
        str | None, Query(max_length=50, description="名称关键词")
    ] = None,
    category_id: Annotated[int | None, Query(gt=0, description="分类id")] = None,
    page: Annotated[int, Query(ge=1, description="页码")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="每页条数")] = 10,
):
    page_data = product_service.get_page_products(
        db= db,
        keyword= keyword,
        category_id=category_id,
        page= page,
        page_size= page_size,
    )
    return Response.success(data=ProductPageResponse.model_validate(page_data))

@router.get("/count", response_model=Response, summary="统计商品数量")
def get_count_product(
    db: Annotated[Session, Depends(get_db)]
    ):
    return Response.success(
        data= ProductCountResponse(
            total=product_service.count_product(db)
        )
    )

@router.get("/{product_id}", response_model=Response, summary="查询单个商品信息")
def get_product(
    product_id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
):
    product = product_service.get_product(db, product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="商品不存在")
    return Response.success(data=ProductResponse.model_validate(product))
