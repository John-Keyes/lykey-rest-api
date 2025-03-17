from fastapi import APIRouter, Depends, HTTPException;
from lib.database.mysql import SessionLocal, GetDb, settings, engine;
from typing import Annotated;
from lib.models.auth import Role
from sqlalchemy.orm import Session;
from routers.auth import GetCurrentUser;
from starlette import status;
from lib.database.models import Users;
from lib.helpers.auth import GenerateCode, AuthenticateUser, CreateAccessToken, GetCurrentUser, bcryptContext
from lib.models.users import User

accountRouter = APIRouter(
    prefix="/account",
    tags=["account"]
)

dbDependency = Annotated[Session, Depends(GetDb)]
accountDependency = Annotated[dict, Depends(GetCurrentUser)]

@accountRouter.get("/", status_code=status.HTTP_200_OK)
async def GetProfile(account: accountDependency):
    if account is None:
        raise HTTPException(status_code=401, detail="Error: Get Users Failed")
    return account

@accountRouter.put("/", status_code=status.HTTP_200_OK)
async def UpdateProfile(account: accountDependency, db: dbDependency, formData: User):
    if not formData:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail="Error: Vacant form data")
    if account is None:
        raise HTTPException(status_code=401, detail="Error: Get Users Failed")
    account.email = formData.email
    account.password = formData.password
    account.isVerified = formData.isVerified
    account.role = formData.role
    account.country = formData.country
    account.pic = formData.pic
    db.commit()
    db.refresh(account)
    return formData

@accountRouter.delete("/", status_code=status.HTTP_200_OK)
async def DeleteUser(db: dbDependency, account: accountDependency):
    await db.query(Users).filter(Users.userId == account.userId)
    result = User(
        userId = -1,
        email = "",
        password = "",
        isVerified = "",
        role = Role.GUEST,
        country = "",
        pic = ""
    )
    return result