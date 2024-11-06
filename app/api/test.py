from fastapi import APIRouter, Depends

test_router = APIRouter(prefix="/test", tags=["user"])

# get test
@test_router.get("/sample")
async def routeHello():
    return "Test success"