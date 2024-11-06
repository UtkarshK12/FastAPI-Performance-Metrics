from models import MessageModel
from database import PgDatabase
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

def getAllRecords() -> list:
    getAllRecordsQuery = "SELECT id, message FROM messages"
    db = PgDatabase()
    
    try:
        with db.get_connection() as (conn, cur):
            cur.execute(getAllRecordsQuery)
            results = cur.fetchall()
            return [
                {
                    "id": row[0],
                    "message": row[1]
                }
                for row in results
            ]
    except Exception as e:
        logger.error(f"Error getting records: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

def insertIntoDB(payload: MessageModel) -> MessageModel:
    insertIntoDbQuery = """
        INSERT INTO messages (message) 
        VALUES (%s) 
        RETURNING id, message;
    """
    db = PgDatabase()
    
    try:
        with db.get_connection() as (conn, cur):
            cur.execute(insertIntoDbQuery, (payload.message,))
            result = cur.fetchone()
            conn.commit()
            
            if result is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to insert record"
                )
                
            return MessageModel(
                id=result[0],
                message=result[1]
            )
    except Exception as e:
        logger.error(f"Error inserting record: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )