from fastapi import FastAPI, HTTPException,status
from database import createTable, drop_tables, health_check
from api.test import test_router

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
        
app.include_router(test_router)