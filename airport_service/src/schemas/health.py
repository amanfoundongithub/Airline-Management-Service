from pydantic import BaseModel
from datetime import datetime

class PingResponse(BaseModel):
    timestamp : datetime

    # Information on server
    name : str
    version : str
    status : str

class HealthCheckResponse(BaseModel):
    timestamp : datetime
    name : str
    version : str
    status : str