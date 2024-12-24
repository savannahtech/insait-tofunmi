from typing import Dict, Any
from app.handlers import APIError
from pydantic import ValidationError

def validate_request_json(json_data: Dict[str, Any], model_class):
    try:
        return model_class.parse_obj(json_data)
    except ValidationError as e:
        raise APIError(
            message="Validation error",
            status_code=422,
            payload={"details": e.errors()}
        )