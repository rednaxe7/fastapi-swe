from fastapi import FastAPI
from datetime import datetime
from api.database import Database
from api.schemas import UserCreate, UserUpdate 

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "fastapi-swe-v0.2.0"}

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
    insert_query = """
        INSERT INTO users (username, email, first_name, last_name, role, active, created_at, updated_at)
        VALUES (:username, :email, :first_name, :last_name, :role, :active, :created_at, :updated_at);
    """
    last_insert_id_query = "SELECT LAST_INSERT_ID();"

    try:
        # Obtener el tiempo actual
        date_now = datetime.now()

        # Convertir los datos del usuario en un diccionario
        user_data = user.dict()
        user_data["created_at"] = date_now
        user_data["updated_at"] = date_now

        with Database() as db:
            # Ejecutar la inserción del nuevo usuario
            db.execute_query(insert_query, user_data)
            
            # Obtener el último ID insertado **antes de hacer commit**
            result = db.execute_query(last_insert_id_query)
            new_user_id = result[0][0] if result else None

            if new_user_id is None:
                raise HTTPException(status_code=500, detail="Failed to retrieve the user ID")

            # Hacer el commit después de obtener el ID
            db.commit()

            return {"message": "User created successfully", "user_id": new_user_id}
    
    except Exception as e:
        print(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Error inserting user into database")

    
@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    try:
        user_data = user.dict(exclude_unset=True)
        
        if not user_data:
            raise HTTPException(status_code=400, detail="No fields to update")

        user_data["updated_at"] = datetime.now()
        user_data["id"] = user_id

        # Construcción dinámica del SET
        set_clause = ", ".join([f"{key} = :{key}" for key in user_data if key != "id"])
        query = f"UPDATE users SET {set_clause} WHERE id = :id"

        with Database() as db:
            db.execute_query(query, user_data)
            db.commit()

        return {"message": "User updated successfully"}
    except Exception as e:
        print(f"Error updating user: {e}")
        raise HTTPException(status_code=500, detail="Error updating user in database")