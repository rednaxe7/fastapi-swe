from fastapi import FastAPI
from api.database import Database
from api.schemas import UserCreate 

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "fastapi-swe-v0.1.3"}

@app.get("/health/db")
def health_check_db():
    try:
        with Database() as db:
            db.execute_query("SELECT 1")
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        print(f"Health Check Error: {e}")
        return {"status": "error", "db": "not connected"}
    
@app.post("/users")
def create_user(user: UserCreate):
    query = """
        INSERT INTO users (username, email, first_name, last_name, role, active)
        VALUES (:username, :email, :first_name, :last_name, :role, :active)
    """
    try:
        with Database() as db:
            db.execute_query(query, user.dict())
            db.commit()
        return {"message": "User created successfully"}
    except Exception as e:
        print(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Error inserting user into database")