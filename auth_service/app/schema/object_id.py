from bson import ObjectId


# --------- PYDANTIC METHOD TO HANDLE OBJECT ID -----------
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate 

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid Object Id")
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema : dict):
        field_schema.update(type = "string")
