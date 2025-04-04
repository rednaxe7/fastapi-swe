import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

class Database:
    def __init__(self):
        self.engine = self.connect()

    def connect(self):
        try:
            # Lee la URL de la base de datos desde las variables de entorno
            database_url = os.getenv("DATABASE_URL")
            return create_engine(database_url)
        except SQLAlchemyError as e:
            print(f"DB Connection Error: {e}")
            return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_connection()

    def execute_query(self, query, params=None):
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query), params)
                return result.fetchall()
        except SQLAlchemyError as e:
            print(f"Query Execution Error: {e}")
            return None

    def close_connection(self):
        if self.engine:
            self.engine.dispose()
