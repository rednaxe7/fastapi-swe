import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

class Database:
    def __init__(self):
        self.engine = self.connect()
        self.connection = None  # Para uso en commit/rollback manual

    def connect(self):
        try:
            database_url = os.getenv("DATABASE_URL")
            return create_engine(database_url)
        except SQLAlchemyError as e:
            print(f"DB Connection Error: {e}")
            return None

    def __enter__(self):
        self.connection = self.engine.connect()
        self.transaction = self.connection.begin()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self.close_connection()

    def execute_query(self, query, params=None):
        try:
            result = self.connection.execute(text(query), params)
            return result.fetchall() if result.returns_rows else None
        except SQLAlchemyError as e:
            print(f"Query Execution Error: {e}")
            return None

    def commit(self):
        try:
            if self.transaction.is_active:
                self.transaction.commit()
        except SQLAlchemyError as e:
            print(f"Commit Error: {e}")

    def rollback(self):
        try:
            if self.transaction.is_active:
                self.transaction.rollback()
        except SQLAlchemyError as e:
            print(f"Rollback Error: {e}")

    def close_connection(self):
        if self.connection:
            self.connection.close()
        if self.engine:
            self.engine.dispose()
