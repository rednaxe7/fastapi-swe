from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "fastapi-swe-v0.0.3"}



#from sqlalchemy import create_engine

#DATABASE_URL = "mysql+pymysql://root:supersecret@containers-us-west-XX.railway.app:XXXX/railway"

#engine = create_engine(DATABASE_URL)
