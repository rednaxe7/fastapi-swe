import logging
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.api import user_routes
#from src.db import models  
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
    return {"message": "fastapi-swe-v1.0.0"}


app.include_router(user_routes.router)

# Manejo global de errores 500
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception): # pragma: no cover
    logger.exception(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "codigo": "99",
            "error": "Sorry, an unexpected error has occurred. Please try again later."
        },
    )