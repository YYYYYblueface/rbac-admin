from typing import Any, Optional

from pydantic import BaseModel


class APIResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Optional[Any] = None

    model_config = {"from_attributes": True}


def success(data: Any = None, message: str = "success") -> dict:
    return {"code": 200, "message": message, "data": data}


def fail(code: int = 400, message: str = "fail", data: Any = None) -> dict:
    return {"code": code, "message": message, "data": data}