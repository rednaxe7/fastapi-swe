import logging
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI
from src.api import user_routes
from src.db.database import Base, engine

# Middleware para registrar las solicitudes
class LogRequestsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response

# Configuración básica del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(LogRequestsMiddleware)

# Ruta principal
@app.get("/")
def read_root():
    logger.info("Root endpoint hit")
    return {"message": "fastapi-swe-v0.2.7"}

app.include_router(user_routes.router)