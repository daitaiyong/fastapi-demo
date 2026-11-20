from xml.sax import handler

from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as starletteHTTPException
from pydantic import BaseModel, Field
from sqlalchemy.exc import SQLAlchemyError
from app.api import router as api_router

from app.common.exceptions import (
    BusinessError,
    handle_business_error,
    handle_database_error,
    handle_http_error,
    handle_validation_error,
    handle_unexpected_error,
)
from app.common.response import Response

app = FastAPI()

exception_handlers = {
    BusinessError: handle_business_error,
    SQLAlchemyError: handle_database_error,
    starletteHTTPException: handle_http_error,
    RequestValidationError: handle_validation_error,
    Exception: handle_unexpected_error,
}

for exc_class, handler in exception_handlers.items():
    app.add_exception_handler(exc_class, handler)
    
app.include_router(api_router)


@app.get("/")
def read_root():
    return {"message": "fastapi服务正在运行中"}