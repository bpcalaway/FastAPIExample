from fastapi import FastAPI
from routers.admin import router as admin_router
from routers.turf import router as turf_router
from routers.user import router as user_router


app = FastAPI()
app.include_router(admin_router)
app.include_router(turf_router)
app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "This is the base address of the API for managing the location data of the app"}
