import logging
from os import name
from sqlalchemy import select, func

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.common.exceptions import BusinessError
from app.models import Category,Product
from app.schemas.category import CategoryCreateRequest, CategoryUpdateRequest

logger = logging.getLogger(__name__)

def create_category(db: Session, payload: CategoryCreateRequest) -> Category:
    name = payload.name.strip()
    if not name:
        raise BusinessError("分类名称不能为空")

    statement = select(Category.id).where(Category.name == name)
    exsist_id = db.scalar(statement)
    if exsist_id is not None:
        raise BusinessError("分类名称已经存在", code=409)
    
    category = Category(name= name)
    try:
        db.add(category)
        db.commit()
        db.refresh(category)
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("新增分类数据库操作失败")
        if isinstance(exc, IntegrityError) and exc.orig is not None:
            if exc.orig.args and exc.orig.args[0] == 1062:
                raise BusinessError("分类名称已经存在", code=409) from exc
        raise
    return category

def update_category(db: Session, payload: CategoryUpdateRequest, category_id: int) -> Category:
    category = db.get(Category, category_id)
    if not category:
        raise BusinessError("分类不存在", code=404)
    category.name = payload.name
    try:
        db.commit()
        db.refresh(category)
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("修改分类数据库操作失败")
        if isinstance(exc, IntegrityError) and exc.orig is not None:
            if exc.orig.args and exc.orig.args[0] == 1062:
                raise BusinessError("分类名称已经存在", code=409) from exc
        raise
    return category

def delete_category(db: Session, category_id: int):
    category = db.get(Category, category_id)
    if not category:
        raise BusinessError("分类不存在", code=404)
    product_count = db.scalar(
        select(func.count(Product.id)).where(Product.category_id == category_id)
        ) or 0
    if product_count > 0:
        raise BusinessError(message="分类下有商品存在，不能删除", code=409)
    try:
        db.delete(category)
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("修改分类数据库操作失败")


def get_category(db: Session):
    try:
        statement = select(Category).order_by(Category.id.desc())
        return db.scalars(statement).all()
    except SQLAlchemyError as exc:
        logger.exception("查询分类列表失败")
        raise BusinessError("查询分类失败，请稍后再试", code=500) from exc

def get_category_statistics(db: Session):
    try:
        statement = (
            select(
                Category.id,
                Category.name,
                func.count(Product.id).label("product_count"),
            )
            .outerjoin(Product, Product.category_id == Category.id)
            .group_by(Category.id, Category.name)
            .order_by(Category.id.asc())
        )
        rows = db.execute(statement).all()
        return [
            {
                "id": category_id,
                "name": name,
                "product_count": product_count,
            }
            for category_id, name, product_count in rows
        ]
    except SQLAlchemyError as exc:
        logger.exception("统计分类商品数量失败")
        raise BusinessError("统计分类商品数量失败，请重新尝试", code=500) from exc