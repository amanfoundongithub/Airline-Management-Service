from bson import ObjectId
from typing import Any

class PyObjectId(str):
    """
    Pydantic v2 compatible ObjectId wrapper.
    Internally stored as `str`, but accepts `ObjectId` or `str`.
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema

        return core_schema.no_info_plain_validator_function(
            cls.validate,
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def validate(cls, v: Any) -> "PyObjectId":
        if isinstance(v, ObjectId):
            return cls(str(v))
        if isinstance(v, str):
            if ObjectId.is_valid(v):
                return cls(v)
        raise ValueError("Invalid ObjectId")
