from fastapi import FastAPI
from api.database import Database

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "fastapi-swe-v0.1.0"}

@app.get("/health/db")
def health_check_db():
    try:
        with Database() as db:
            db.execute_query("SELECT 1")
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        print(f"Health Check Error: {e}")
        return {"status": "error", "db": "not connected"}