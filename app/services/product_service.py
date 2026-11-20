
import logging

from sqlalchemy import func,select
from app.schemas.product import ProductCreateRequest, ProductResponse, ProductUpdateRequest

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.common.exceptions import BusinessError
from app.models import Product, Category, category


logger = logging.getLogger(__name__)

def create_product(db: Session, payload: ProductCreateRequest) -> Product:
    name = payload.name.strip()
    if not name:
        raise BusinessError("商品名称不能为空")

    try:
        category = db.get(Category, payload.category_id)
        if category is None:
            raise BusinessError("商品分类不存在")
        
        product = Product(**payload.model_dump())
        product.name = name
        db.add(product)
        db.commit()
        db.refresh(product)
    except SQLAlchemyError:
        db.rollback()
        logger.exception("新增商品数据库操作失败")
        raise
    return product

def update_product(db: Session, payload: ProductUpdateRequest, product_id:int) -> Product:
    try:
        product = db.get(Product, product_id)
        if product is None:
            raise BusinessError(message="未找到商品信息", code=404)
        changes = payload.model_dump(exclude_unset=True)
        if not changes:
            raise BusinessError("至少提交一个修改的字段")
        for field, value in changes.items():
            if value is None:
                raise BusinessError(f"字段{field}的值不允许为null")

        if "name" in changes:
            if not changes["name"]:
                raise BusinessError("商品名称不能只包含空白")

        if "category_id" in changes:
            if db.get(Category, changes["category_id"]) is None:
                raise BusinessError("商品分类不存在")

        for field, value in changes.items():
            setattr(product, field, value)
        db.commit()
        db.refresh(product)
    except SQLAlchemyError:
        logger.exception("修改商品数据库操作失败")
        raise BusinessError("商品更新失败")
    return product

def delete_product(db: Session, product_id:int):
    product = db.get(Product, product_id)
    if product is None:
        raise BusinessError(message="商品不存在", code=404)
    try:
        db.delete(product)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        logger.exception("商品删除数据库操作失败")
        raise BusinessError("商品删除失败")

def get_page_products(
        db: Session,
        keyword: str | None = None,
        category_id: int | None = None,
        page: int = 1,
        page_size: int = 10,
):
    keyword = (keyword or "").strip()
    filters = []
    if keyword:
        filters.append(Product.name.contains(keyword, autoescape=True))
    if category_id is not None:
        filters.append(Product.category_id == category_id)

    try:
        total_statement = select(func.count(Product.id)).where(*filters)
        total = db.scalar(total_statement)

        statement = (
            select(Product, Category.name.label("category_name"))
            .join(Category, Product.category_id == Category.id)
            .where(*filters)
            .order_by(Product.id.desc())
            .offset((page-1) * page_size)
            .limit(page_size)
        )
        rows = db.execute(statement).all()
        items = [
            {
            **ProductResponse.model_validate(product).model_dump(),
            "category_name": category_name,
            }
            for product, category_name in rows
        ]
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
        }
    except SQLAlchemyError as exc:
        logger.exception("查询商品数量失败")
        raise BusinessError("查询商品数量失败，请稍后再试", code=500) from exc

def count_product(db: Session) -> int:
    try:
        statement = select(func.count(Product.id))
        return db.execute(statement).scalars().one()
    except SQLAlchemyError as exc:
        logger.exception("统计商品数量失败")
        raise BusinessError("统计商品数量失败，请稍后再试", code=500) from exc

def get_product(db:Session, product_id: int):
    try:
        return db.get(Product, product_id)
    except SQLAlchemyError as exc:
        logger.exception("查询商品详情失败")
        raise BusinessError("查询商品失败，请稍后再试", code=500) from exc