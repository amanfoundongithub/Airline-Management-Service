from fastapi           import FastAPI
from src.api.v1.router import router as v1_router


# Initialize the FastAPI application
app = FastAPI()

# Add the router to the main application
app.include_router(v1_router)