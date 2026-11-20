from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.common.response import Response
from app.schemas.category import CategoryCreateRequest, CategoryUpdateRequest, CategoryResponse, CategoryStatisticResponse
from app.services import category_service 

router = APIRouter(prefix="/categories", tags=["分类相关接口"])

@router.post("", response_model=Response, summary="创建商品分类")
def create_category(
    payload: CategoryCreateRequest, 
    db: Annotated[Session, Depends(get_db)],
    ):
    return Response.success(
        data=CategoryResponse.model_validate(
            category_service.create_category(db, payload))
    )

@router.patch("/{category_id}", response_model=Response, summary="更新商品分类")
def update_category(
    payload: CategoryUpdateRequest, 
    category_id: int,
    db: Annotated[Session, Depends(get_db)],
    ):
    update_category = category_service.update_category(db, payload, category_id)
    return Response.success(
        data=CategoryResponse.model_validate(update_category)
    )

@router.delete("/{category_id}", response_model=Response, summary="删除商品分类")
def delete_category(
    category_id: int,
    db: Annotated[Session, Depends(get_db)],
    ):
    update_category = category_service.delete_category(db, category_id)
    return Response.success(update_category)

@router.get("", response_model=Response, summary="查询分类")
def get_category(
    db: Annotated[Session, Depends(get_db)],
    ):
    return Response.success(
        data=[CategoryResponse.model_validate(item)
              for item in category_service.get_category(db)
        ]
    )

@router.get("/statistics", response_model=Response, summary="统计分类商品的数量")
def get_category_statistics(
    db: Annotated[Session, Depends(get_db)],
    ):
    return Response.success(
        data=[CategoryStatisticResponse.model_validate(item)
              for item in category_service.get_category_statistics(db)
        ]
    )