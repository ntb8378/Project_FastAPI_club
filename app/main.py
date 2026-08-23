from fastapi import FastAPI, Request, HTTPException
from app.db.database import Base, engine
from app.models.user import UsersModel
from app.models.club import ClubsModel, ClubMembersModel
from app.models.activity import ClubActivitiesModel
from app.routers import router
from fastapi.responses import JSONResponse


app = FastAPI()

app.include_router(router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return{
        "message" : "Kết nối thành công!"
    }

@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.status_code,
            "message": exc.detail
        }
    )