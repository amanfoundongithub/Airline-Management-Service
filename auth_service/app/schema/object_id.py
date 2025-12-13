from bson import ObjectId

from typing import Any, Annotated
from pydantic import BeforeValidator


# --------- PYDANTIC METHOD TO HANDLE OBJECT ID -----------
def validate_object_id(v: Any) -> ObjectId:
    """
    Validates input and converts it to a bson.ObjectId instance.
    """
    if isinstance(v, ObjectId):
        return v
    if isinstance(v, str) and ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId format")

PyObjectId = Annotated[
    ObjectId, 
    BeforeValidator(validate_object_id) 
]