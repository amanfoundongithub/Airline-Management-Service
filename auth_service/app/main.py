from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from app.db.client import connect_with_mongo, disconnect_with_mongo

from app.api.v1.router import router as v1_router

# App
app = FastAPI(title = "Airline Auth Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,            
    allow_methods=["*"],                
    allow_headers=["*"],
)

# Hooks
app.add_event_handler("startup", connect_with_mongo)
app.add_event_handler("shutdown", disconnect_with_mongo)

# Routers
app.include_router(v1_router)

# Check if the server is up and which version is running
@app.get("/")
def read_root():
    return {
        "timestamp" : datetime.now(),
        "status" : "Auth Service running",
        "version" : "v1"
    }