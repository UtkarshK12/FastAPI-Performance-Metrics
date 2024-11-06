from fastapi import FastAPI, HTTPException,status
from dao.DB_commons import createTable, drop_tables, health_check
from api.test import test_router
from dao.messagesDao import getAllRecords, insertIntoDB
from models import MessageModel

app=FastAPI()


@app.post("/initDB")
async def initDB():
    try:
        drop_tables()
        createTable()
        return {"message": "tables have been created"}
    except Exception as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f"Error {e}"
        )
    
@app.get("/hello")
async def routeHello():
    return "Hello"


@app.get("/health")
async def route_health_check():
    try:
        health_check()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database not healthy: {str(e)}"
        )
    

@app.get("/getAllMessages")
async def getAllMessages():
    try:
        return getAllRecords()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database not healthy: {str(e)}"
        )
    
@app.post("/insertRecord", response_model=MessageModel)
async def insertRecord(message: MessageModel):
    try:
        result = insertIntoDB(message)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to insert record"
            )
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
app.include_router(test_router)