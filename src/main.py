from fastapi import FastAPI
from src.api import user_routes
from src.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_routes.router)