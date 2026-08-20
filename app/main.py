from fastapi import FastAPI

from app.db.database import Base, engine

from app.models.user import UsersModel
from app.models.club import ClubsModel, ClubMembersModel
from app.models.activity import ClubActivitiesModel


app = FastAPI()

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