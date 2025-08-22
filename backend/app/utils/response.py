from fastapi.responses import JSONResponse
from app.utils.status_code import StatusCode
from pydantic import BaseModel
from typing import Optional, Any, Dict, List, Union
import json
import math


from fastapi.responses import JSONResponse

class ResponseWrapper:
    @staticmethod
    def success(data=None, msg="success", code=0):
        return SafeJSONResponse(content={
            "code": code,
            "msg": msg,
            "data": data
        })

    @staticmethod
    def error(msg="error", code=500, data=None):
        return SafeJSONResponse(content={
            "code": code,
            "msg": str(msg),
            "data": data
        })



class SafeJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        def sanitize_floats(obj: Any) -> Any:
            if isinstance(obj, dict):
                return {k: sanitize_floats(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [sanitize_floats(item) for item in obj]
            elif isinstance(obj, float):
                if math.isnan(obj) or math.isinf(obj):
                    return None
                return obj
            return obj

        # 清理内容中的非法浮点数
        cleaned_content = sanitize_floats(content)
        
        return json.dumps(
            cleaned_content,
            ensure_ascii=False,
            allow_nan=False,  # 防止NaN值
            separators=(",", ":"),
            default=str,  # 处理无法序列化的对象
        ).encode("utf-8")