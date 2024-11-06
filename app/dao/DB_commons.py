from database import PgDatabase
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)
message_tbl = "messages"

def createTable():
    db = PgDatabase()
    try:
        with db.get_connection() as (conn, cur):
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {message_tbl} (
                    id SERIAL PRIMARY KEY,
                    message VARCHAR NOT NULL
                )
            """)
            conn.commit()
            logger.info("Tables created successfully")
    except Exception as e:
        logger.error(f"Error creating table: {e}")
        raise

def drop_tables():
    db = PgDatabase()
    try:
        with db.get_connection() as (conn, cur):
            cur.execute(f"DROP TABLE IF EXISTS {message_tbl} CASCADE;")
            conn.commit()
            logger.info("Tables dropped successfully")
    except Exception as e:
        logger.error(f"Error dropping tables: {e}")
        raise

def health_check():
    db = PgDatabase()
    try:
        with db.get_connection() as (conn, cur):
            cur.execute("SELECT 1")
            result = cur.fetchone()
            return result is not None
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database not healthy: {str(e)}"
        )