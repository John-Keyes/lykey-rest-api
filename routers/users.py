from sqlalchemy import select;
from fastapi import APIRouter, Depends, HTTPException;
from lib.database.mysql import SessionLocal, GetDb, settings, engine;
from typing import Annotated;
from sqlalchemy.orm import Session;
from routers.auth import GetCurrentUser;
from starlette import status;
from lib.database.models import Users;
from lib.helpers.auth import GenerateCode, AuthenticateUser, CreateAccessToken, GetCurrentUser, bcryptContext
from lib.models.users import SafeUser;

userRouter = APIRouter(
    prefix="/users",
    tags=["users"]
)

dbDependency = Annotated[Session, Depends(GetDb)]

@userRouter.get("/", status_code=status.HTTP_200_OK)
async def GetSafeUsers(db: dbDependency):
    stmt = select(Users.userId, Users.email, Users.country, Users.pic).where(Users.isVerified == 'T')
    users = []
    for row in db.execute(stmt):
        users.append(SafeUser(
            userId = row.userId,
            email = row.email,
            country = row.country,
            pic = row.pic
        ))
    return users

@userRouter.get("/{userId}", status_code=status.HTTP_200_OK)
async def GetSafeUser(userId: int, db: dbDependency):
    #user = db.query(Users).filter((Users.userId == userId) and (Users.isVerified == 'T')).first()
    stmt = select(Users.userId, Users.email, Users.country, Users.pic).where(Users.userId == userId).where(Users.isVerified == 'T')
    user = db.execute(stmt).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Error: Get User Failed")
    return SafeUser(
        userId = user.userId,
        email = user.email,
        country = user.country,
        pic = user.pic
    )