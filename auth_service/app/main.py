from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.client import connect_with_mongo, disconnect_with_mongo

import api.v1.user_router as user_router

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
app.include_router(user_router.router, prefix = "/api/v1")


@app.get("/")
def read_root():
    return {
        "status" : "Auth Service running",
        "version" : "v1"
    }

