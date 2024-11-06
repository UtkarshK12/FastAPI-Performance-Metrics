from abc import ABC, abstractmethod
import os
import dotenv
from pathlib import Path
from fastapi import HTTPException,status
import psycopg

BASE_DIR=Path(__file__).resolve().parent.parent
dotenv.load_dotenv(BASE_DIR/".env")

class Database(ABC):

    def __init__(self,driver):
        self.driver=driver
    
    @abstractmethod
    def connect_to_database(self):
        raise NotImplementedError()
    
    def __enter__(self):
        self.connection = self.connect_to_database()
        self.cursor=self.connection.cursor()
        return self

    def __exit__(self, exception_type, exc_val, traceback):
        self.cursor.close()
        self.connection.close()


class PgDatabase(Database):

    def __init__(self)->None:
        self.driver=psycopg
        super().__init__(self.driver)

    def connect_to_database(self):
        try:
            return self.driver.connect(
                host=os.getenv("DB_HOST"),
                port=int(os.getenv("DB_PORT", "5432")),  # Convert port to int
                user=os.getenv("DB_USERNAME"),
                password=os.getenv("DB_PASSWORD"),
                dbname=os.getenv("DB_NAME")
            )
        except Exception as e:
            print(f"Connection error: {e}")
            raise

    

message_tbl="messages"

def createTable():
    with PgDatabase() as db:
        db.cursor.execute(f"""CREATE TABLE {message_tbl} (id SERIAL PRIMARY KEY, context VARCHAR)""")
        db.connection.commit()
        print("tables create")


def drop_tables():
    with PgDatabase() as db:
        db.cursor.execute(f"DROP TABLE IF EXISTS {message_tbl} CASCADE;")
        db.connection.commit()
        print("Tables are dropped...")


def health_check():
    with PgDatabase() as db:
        db.cursor.execute(f"SELECT 1")
        db.connection.commit()
        print("db health checked passed...")

