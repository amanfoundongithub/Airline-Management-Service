from fastapi import FastAPI
from db.client import connect_with_mongo, disconnect_with_mongo


# App
app = FastAPI()

# Hooks
app.add_event_handler("startup", connect_with_mongo)
app.add_event_handler("shutdown", disconnect_with_mongo)

