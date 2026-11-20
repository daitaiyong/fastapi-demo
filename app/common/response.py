"""统一响应数据结构"""

from typing import Any

from pydantic import BaseModel


class Response(BaseModel):
    code: int
    message: str
    data: Any = None

    @classmethod
    def success(cls, data: Any = None, message: str = "请求成功"):
        return cls(code=200 , message= message, data=data)

    @classmethod
    def error(cls, code: int, message: str, data: Any = None):
        return cls(code= code, message= message, data=data)