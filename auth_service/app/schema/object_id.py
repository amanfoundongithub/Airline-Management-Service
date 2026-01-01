from bson import ObjectId

from typing import Annotated
from pydantic import PlainSerializer


# --------- PYDANTIC METHOD TO HANDLE OBJECT ID -----------
PyObjectId = Annotated[
    ObjectId, 
    PlainSerializer(lambda x: str(x), return_type=str, when_used='json')
]